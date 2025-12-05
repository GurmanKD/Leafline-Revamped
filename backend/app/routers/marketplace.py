from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from .. import models, schemas
from ..deps import get_db_session, get_current_user_from_header

router = APIRouter(
    prefix="/marketplace",
    tags=["marketplace"],
)


@router.post(
    "/listings",
    response_model=schemas.CreditListingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_listing(
    listing_in: schemas.CreditListingCreate,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user_from_header),
) -> schemas.CreditListingOut:
    """
    Create a credit listing for a plantation owned by the current user.

    - Checks ownership
    - Ensures enough available credits
    - Moves credits from available -> locked
    """
    if current_user.role != models.UserRole.PLANTATION_OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only plantation owners can create listings.",
        )

    # Fetch plantation
    stmt = select(models.Plantation).where(models.Plantation.id == listing_in.plantation_id)
    plantation = db.execute(stmt).scalar_one_or_none()

    if plantation is None:
        raise HTTPException(status_code=404, detail="Plantation not found.")

    if plantation.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not own this plantation.")

    balance = plantation.credit_balance
    if balance is None:
        raise HTTPException(status_code=400, detail="Credit balance not initialized for this plantation.")

    if balance.available_credits < listing_in.credits:
        raise HTTPException(
            status_code=400,
            detail="Not enough available credits to list.",
        )

    # Move credits from available to locked
    balance.available_credits -= listing_in.credits
    balance.locked_credits += listing_in.credits

    listing = models.CreditListing(
        plantation_id=plantation.id,
        seller_id=current_user.id,
        total_credits=listing_in.credits,
        remaining_credits=listing_in.credits,
        price_per_credit=listing_in.price_per_credit,
        status=models.ListingStatus.ACTIVE,
    )

    db.add(listing)
    db.commit()
    db.refresh(listing)

    return schemas.CreditListingOut.model_validate(listing)


@router.get("/listings", response_model=List[schemas.CreditListingOut])
def list_active_listings(
    db: Session = Depends(get_db_session),
) -> List[schemas.CreditListingOut]:
    """
    List all active or partially filled listings.
    """
    stmt = select(models.CreditListing).where(
        models.CreditListing.status.in_(
            [models.ListingStatus.ACTIVE, models.ListingStatus.PARTIALLY_FILLED]
        )
    )
    listings = db.execute(stmt).scalars().all()
    return [schemas.CreditListingOut.model_validate(l) for l in listings]


@router.post(
    "/trades",
    response_model=schemas.TradeOut,
    status_code=status.HTTP_201_CREATED,
)
def create_trade(
    trade_in: schemas.TradeCreate,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user_from_header),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> schemas.TradeOut:
    """
    Buy credits from a listing.

    Uses an Idempotency-Key header to ensure that retrying the same request
    does not create duplicate trades.

    Flow:
    - If a trade with the same idempotency_key exists, returns it directly.
    - Otherwise:
        * validates listing and credits
        * creates trade
        * updates listing + seller balance
    """
    if current_user.role != models.UserRole.INDUSTRY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only industry users can buy credits.",
        )

    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header is required.",
        )

    # Check for existing trade with same key (idempotency)
    stmt_existing = select(models.Trade).where(models.Trade.idempotency_key == idempotency_key)
    existing_trade = db.execute(stmt_existing).scalar_one_or_none()

    if existing_trade is not None:
        # Return the previous trade: idempotent behavior
        return schemas.TradeOut.model_validate(existing_trade)

    # Fetch listing
    stmt_listing = select(models.CreditListing).where(models.CreditListing.id == trade_in.listing_id)
    listing = db.execute(stmt_listing).scalar_one_or_none()

    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found.")

    if listing.status in [models.ListingStatus.FILLED, models.ListingStatus.CANCELLED]:
        raise HTTPException(status_code=400, detail="Listing is not available for trading.")

    if trade_in.credits > listing.remaining_credits:
        raise HTTPException(
            status_code=400,
            detail="Not enough remaining credits in this listing.",
        )

    # Compute total price
    total_price = trade_in.credits * listing.price_per_credit

    # Update listing
    listing.remaining_credits -= trade_in.credits
    if listing.remaining_credits == 0:
        listing.status = models.ListingStatus.FILLED
    else:
        listing.status = models.ListingStatus.PARTIALLY_FILLED

    # Update seller balance: locked_credits decreases
    plantation = listing.plantation
    balance = plantation.credit_balance
    balance.locked_credits -= trade_in.credits
    # NOTE: We are not increasing seller available here; once sold, credits are considered transferred.

    # Create trade
    trade = models.Trade(
        listing_id=listing.id,
        buyer_id=current_user.id,
        credits=trade_in.credits,
        total_price=total_price,
        idempotency_key=idempotency_key,
    )

    db.add(trade)
    db.commit()
    db.refresh(trade)

    return schemas.TradeOut.model_validate(trade)
