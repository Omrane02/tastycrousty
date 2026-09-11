from fastapi import FastAPI

from src.modules.health.router import router as health_router

app = FastAPI(title="Ytasty Crousty API", version="0.1.0")

app.include_router(health_router)