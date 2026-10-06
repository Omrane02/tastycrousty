import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.realtime import sio
from src.db.migration import run_migration
from src.db.seed import seed_data
from src.modules.auth.router import router as auth_router
from src.modules.health.router import router as health_router
from src.modules.orders.router import router as orders_router
from src.modules.products.router import router as products_router
from src.modules.restaurants.router import router as restaurants_router
from src.modules.users.router import router as users_router

app = FastAPI(title="Ytasty Crousty API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ytasty-crousty-frontend.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

run_migration()

seed_data()

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(restaurants_router)
app.include_router(products_router)
app.include_router(orders_router)

# Tout à la fin : Socket.io enveloppe l'application FastAPI complète.
# Le nom `app` est conservé, donc la commande uvicorn ne change pas.
fastapi_app = app
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)