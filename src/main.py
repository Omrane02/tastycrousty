from fastapi import FastAPI

from src.modules.health.router import router as health_router
from src.db.migration import run_migration

app = FastAPI(title="Ytasty Crousty API", version="0.1.0")

run_migration()

seed_data()
app.include_router(health_router)