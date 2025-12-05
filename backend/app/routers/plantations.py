from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from .. import models, schemas
from ..deps import get_db_session, get_current_user_from_header

router = APIRouter(
    prefix="/plantations",
    tags=["plantations"],
)


@router.post(
    "",
    response_model=schemas.PlantationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_plantation(
    plantation_in: schemas.PlantationCreate,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user_from_header),
) -> schemas.PlantationOut:
    """
    Create a new plantation for the current user.

    - Uses the X-User-Id header to determine the owner.
    - Stores the geofence coordinates as JSON.
    - Initializes an associated green credit balance (all zeros).
    """
    coordinates_json = [coord.model_dump() for coord in plantation_in.coordinates]

    plantation = models.Plantation(
        owner_id=current_user.id,
        name=plantation_in.name,
        coordinates_json=coordinates_json,
    )

    db.add(plantation)
    db.flush()  # to get plantation.id before commit

    # Initialize green credit balance for this plantation
    balance = models.GreenCreditBalance(
        plantation_id=plantation.id,
        total_credits=0,
        available_credits=0,
        locked_credits=0,
    )
    db.add(balance)

    db.commit()
    db.refresh(plantation)

    # Map DB model -> Pydantic
    return schemas.PlantationOut(
        id=plantation.id,
        owner_id=plantation.owner_id,
        name=plantation.name,
        coordinates=plantation_in.coordinates,
        created_at=plantation.created_at,
    )


@router.get("", response_model=List[schemas.PlantationOut])
def list_my_plantations(
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user_from_header),
) -> List[schemas.PlantationOut]:
    """
    List all plantations belonging to the current user.
    """
    stmt = select(models.Plantation).where(models.Plantation.owner_id == current_user.id)
    plantations = db.execute(stmt).scalars().all()

    result: List[schemas.PlantationOut] = []
    for p in plantations:
        coords = [schemas.Coordinate(**coord) for coord in p.coordinates_json]
        result.append(
            schemas.PlantationOut(
                id=p.id,
                owner_id=p.owner_id,
                name=p.name,
                coordinates=coords,
                created_at=p.created_at,
            )
        )

    return result


@router.get("/{plantation_id}", response_model=schemas.PlantationOut)
def get_plantation(
    plantation_id: int,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user_from_header),
) -> schemas.PlantationOut:
    """
    Get a single plantation by ID, ensuring it belongs to the current user.
    """
    stmt = select(models.Plantation).where(models.Plantation.id == plantation_id)
    plantation = db.execute(stmt).scalar_one_or_none()

    if plantation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plantation not found.",
        )

    if plantation.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this plantation.",
        )

    coords = [schemas.Coordinate(**coord) for coord in plantation.coordinates_json]

    return schemas.PlantationOut(
        id=plantation.id,
        owner_id=plantation.owner_id,
        name=plantation.name,
        coordinates=coords,
        created_at=plantation.created_at,
    )

@router.get("/{plantation_id}/dashboard", response_model=schemas.PlantationDashboardOut)
def plantation_dashboard(
    plantation_id: int,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user_from_header),
):
    """
    Aggregated view for a plantation:
    - Last ML analysis
    - Credit balance
    - Active credit listings
    """
    # Fetch plantation
    stmt = select(models.Plantation).where(models.Plantation.id == plantation_id)
    plantation = db.execute(stmt).scalar_one_or_none()

    if plantation is None:
        raise HTTPException(status_code=404, detail="Plantation not found.")

    if plantation.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    # Latest analysis (if any)
    latest_analysis = None
    if plantation.analyses:
        latest = sorted(plantation.analyses, key=lambda a: a.analyzed_at)[-1]
        latest_analysis = schemas.PlantationAnalysisOut.model_validate(latest)

    # Credit balance
    balance = plantation.credit_balance
    if balance is None:
        raise HTTPException(status_code=500, detail="Credit balance missing.")

    credit_balance = schemas.GreenCreditBalanceOut.model_validate(balance)

    # Active listings
    stmt_listings = select(models.CreditListing).where(
        models.CreditListing.plantation_id == plantation.id,
        models.CreditListing.status.in_(
            [models.ListingStatus.ACTIVE, models.ListingStatus.PARTIALLY_FILLED]
        ),
    )
    listings = db.execute(stmt_listings).scalars().all()

    listings_out = [schemas.CreditListingOut.model_validate(l) for l in listings]

    plantation_out = schemas.PlantationOut(
        id=plantation.id,
        owner_id=plantation.owner_id,
        name=plantation.name,
        coordinates=[schemas.Coordinate(**c) for c in plantation.coordinates_json],
        created_at=plantation.created_at,
    )

    return schemas.PlantationDashboardOut(
        plantation=plantation_out,
        latest_analysis=latest_analysis,
        credit_balance=credit_balance,
        active_listings=listings_out,
    )

