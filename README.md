# Leafline Revamped

Leafline Revamped is a backend service for a green-credit trading platform that connects:

- **Plantation owners** with high green-credit potential (trees, vegetation, good AQI impact)
- **Industries/factories** that need to buy green credits to offset their pollution

## High-level Features (planned)

- User & role management (plantation owner, industry, admin)
- Plantation onboarding with geofencing (4-corner coordinates)
- Media upload hooks for tree segmentation (OpenCV / ML)
- NDVI & AQI analysis integration
- Green credit computation engine
- Marketplace for listing & trading green credits
- Proper idempotent APIs for trades and payments

## Tech Stack

- Python, FastAPI
- SQLAlchemy, SQLite (can be swapped to Postgres)
- Pydantic for request/response models
- Future: ML modules for NDVI / AQI

## Getting Started

```bash
python -m venv venv
source venv/bin/activate        # Windows: .\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt

uvicorn app.main:app --reload --app-dir backend
