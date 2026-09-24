from fastapi import FastAPI

from src.modules.health.router import router as health_router
from src.modules.orders.router import router as orders_router
from src.modules.products.router import router as products_router
from src.modules.restaurants.router import router as restaurants_router

app = FastAPI(title="Ytasty Crousty API", version="0.1.0")


app.include_router(health_router)
app.include_router(restaurants_router)
app.include_router(products_router)
app.include_router(orders_router)