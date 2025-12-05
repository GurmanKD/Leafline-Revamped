from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from .models import UserRole


class HealthResponse(BaseModel):
    status: str
    project: str


# ==== USER SCHEMAS ====


class UserBase(BaseModel):
    email: str
    full_name: str
    role: UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==== PLANTATION SCHEMAS ====


class Coordinate(BaseModel):
    lat: float
    lng: float


class PlantationBase(BaseModel):
    name: str
    coordinates: List[Coordinate]


class PlantationCreate(PlantationBase):
    pass


class PlantationOut(PlantationBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==== ANALYSIS & CREDITS ====


class PlantationAnalysisOut(BaseModel):
    id: int
    plantation_id: int
    tree_count: Optional[int] = None
    tree_density: Optional[float] = None
    ndvi_mean: Optional[float] = None
    aqi_prediction: Optional[float] = None
    green_credits: Optional[int] = None
    analyzed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GreenCreditBalanceOut(BaseModel):
    id: int
    plantation_id: int
    total_credits: int
    available_credits: int
    locked_credits: int

    model_config = ConfigDict(from_attributes=True)

# ==== ANALYSIS REQUEST ====


class PlantationAnalyzeRequest(BaseModel):
    """
    Input to trigger analysis.
    Later this may include choices like:
    - run_tree_model
    - run_ndvi
    - run_aqi
    """
    force_recompute: bool = False
