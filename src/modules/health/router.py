from fastapi import APIRouter

from src.modules.health import service
from src.modules.health.schema import Health

router = APIRouter(tags=["health"])


@router.get("/health", response_model=Health)
def health() -> Health:

    return service.get_health()