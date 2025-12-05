from fastapi import FastAPI

from .config import settings
from .schemas import HealthResponse


def create_app() -> FastAPI:
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

    # In future commits we’ll include routers here:
    # from .routers import plantations, marketplace, auth, analysis
    # app.include_router(plantations.router, prefix=settings.API_V1_PREFIX)
    # ...

    return app


app = create_app()
