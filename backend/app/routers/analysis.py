from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from .. import models, schemas
from ..deps import get_db_session, get_current_user_from_header
from ..ml_engine import (
    run_fake_tree_model,
    run_fake_ndvi_model,
    run_fake_aqi_model,
    compute_green_credits,
)

router = APIRouter(
    prefix="/plantations",
    tags=["analysis"],
)


@router.post("/{plantation_id}/analyze", status_code=status.HTTP_201_CREATED)
def analyze_plantation(
    plantation_id: int,
    payload: schemas.PlantationAnalyzeRequest,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user_from_header),
):
    """
    Run analysis pipeline for a plantation.

    1. Runs fake ML models.
    2. Computes green credits.
    3. Stores results in DB.
    4. Updates credit balance.
    """
    # Fetch plantation
    stmt = select(models.Plantation).where(models.Plantation.id == plantation_id)
    plantation = db.execute(stmt).scalar_one_or_none()

    if plantation is None:
        raise HTTPException(status_code=404, detail="Plantation not found.")

    if plantation.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized.")

    # Run "ML pipeline"
    tree_result = run_fake_tree_model()
    ndvi = run_fake_ndvi_model()
    aqi = run_fake_aqi_model()

    credits = compute_green_credits(tree_result["tree_count"], ndvi, aqi)

    # Save analysis record
    analysis = models.PlantationAnalysis(
        plantation_id=plantation.id,
        tree_count=tree_result["tree_count"],
        tree_density=tree_result["tree_density"],
        ndvi_mean=ndvi,
        aqi_prediction=aqi,
        green_credits=credits,
    )

    db.add(analysis)

    # Update balance
    balance = plantation.credit_balance
    balance.total_credits += credits
    balance.available_credits += credits

    db.commit()
    db.refresh(analysis)

    return {
        "plantation_id": plantation.id,
        "analysis_id": analysis.id,
        "tree_count": analysis.tree_count,
        "tree_density": analysis.tree_density,
        "ndvi_mean": analysis.ndvi_mean,
        "aqi_prediction": analysis.aqi_prediction,
        "green_credits_added": credits,
        "total_credits": balance.total_credits,
        "available_credits": balance.available_credits,
    }
