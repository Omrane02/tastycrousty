from fastapi import FastAPI

from src.db.seed import seed_data
from src.modules.health.router import router as health_router
from src.db.migration import run_migration
from src.modules.auth.router import router as auth_router
from src.modules.users.router import router as users_router
from src.modules.restaurants.router import router as restaurants_router

app = FastAPI(title="Ytasty Crousty API", version="0.1.0")

run_migration()

seed_data()

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(restaurants_router)