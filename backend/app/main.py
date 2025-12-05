from fastapi import FastAPI

from .config import settings
from .schemas import HealthResponse
from .database import Base, engine


def create_app() -> FastAPI:
    # Create all tables (dev only – for production we'd use Alembic migrations)
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="Backend service for Leafline Revamped – green credit trading platform.",
    )

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    def health_check() -> HealthResponse:
        """
        Simple health check to verify that the API is running.
        """
        return HealthResponse(status="ok", project=settings.PROJECT_NAME)

    # Future:
    # from .routers import plantations, auth, marketplace, analysis
    # app.include_router(plantations.router, prefix=settings.API_V1_PREFIX)
    # ...

    return app


app = create_app()
