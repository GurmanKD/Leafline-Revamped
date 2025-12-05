from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    Float,
    ForeignKey,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class UserRole(str, enum.Enum):
    PLANTATION_OWNER = "PLANTATION_OWNER"
    INDUSTRY = "INDUSTRY"
    ADMIN = "ADMIN"


class User(Base):
    """
    Application user.

    - Plantation owners can register plantations and list green credits.
    - Industry users can buy credits.
    - Admins can monitor the system.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.PLANTATION_OWNER)

    # NEW: store only the password hash, not the raw password
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    plantations: Mapped[List["Plantation"]] = relationship(
        "Plantation",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class Plantation(Base):
    """
    A geofenced plantation belonging to a plantation owner.

    The geofence is represented as a list of coordinates (lat/lng) – typically the 4 corners.
    """
    __tablename__ = "plantations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # We store the polygon as JSON: [{ "lat": ..., "lng": ... }, ...]
    coordinates_json: Mapped[list] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    owner: Mapped[User] = relationship("User", back_populates="plantations")
    analyses: Mapped[List["PlantationAnalysis"]] = relationship(
        "PlantationAnalysis",
        back_populates="plantation",
        cascade="all, delete-orphan",
    )
    credit_balance: Mapped[Optional["GreenCreditBalance"]] = relationship(
        "GreenCreditBalance",
        back_populates="plantation",
        uselist=False,
        cascade="all, delete-orphan",
    )


class PlantationAnalysis(Base):
    """
    Result of running the ML pipeline on a plantation:

    - tree segmentation (tree_count, tree_density)
    - NDVI statistics
    - AQI prediction
    - green_credits computed
    """
    __tablename__ = "plantation_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plantation_id: Mapped[int] = mapped_column(ForeignKey("plantations.id"), nullable=False, index=True)

    tree_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tree_density: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ndvi_mean: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    aqi_prediction: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    green_credits: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    analyzed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    plantation: Mapped[Plantation] = relationship("Plantation", back_populates="analyses")


class GreenCreditBalance(Base):
    """
    Tracks the green-credit balance for a plantation.

    - total_credits: total credits ever assigned
    - available_credits: credits that can still be sold
    - locked_credits: credits locked in active listings/trades
    """
    __tablename__ = "green_credit_balances"
    __table_args__ = (
        UniqueConstraint("plantation_id", name="uq_green_balance_plantation"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plantation_id: Mapped[int] = mapped_column(ForeignKey("plantations.id"), nullable=False, index=True)

    total_credits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    available_credits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    locked_credits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    plantation: Mapped[Plantation] = relationship("Plantation", back_populates="credit_balance")
