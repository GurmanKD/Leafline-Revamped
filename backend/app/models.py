from sqlalchemy import Column, Integer
from .database import Base


class _Placeholder(Base):
    """
    Temporary placeholder model so Alembic / SQLAlchemy have at least
    one mapped class. Will be removed in the next commit when we add real models.
    """
    __tablename__ = "placeholder"

    id = Column(Integer, primary_key=True, index=True)
