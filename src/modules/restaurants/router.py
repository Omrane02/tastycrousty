from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import require_admin
from src.modules.restaurants import service
from src.modules.restaurants.schema import (
    RestaurantAvailabilityUpdate,
    RestaurantRead,
    RestaurantUpdate,
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=list[RestaurantRead])
def list_restaurants() -> list[RestaurantRead]:
    rows = service.get_all_restaurants()
    return [RestaurantRead(**row) for row in rows]


@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int) -> RestaurantRead:
    row = service.get_restaurant(restaurant_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant introuvable")
    return RestaurantRead(**row)


@router.patch("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    current_user: dict = Depends(require_admin),
) -> RestaurantRead:
    row = service.update_restaurant(restaurant_id, data)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant introuvable")
    return RestaurantRead(**row)


@router.patch("/{restaurant_id}/availability", response_model=RestaurantRead)
def update_availability(
    restaurant_id: int,
    data: RestaurantAvailabilityUpdate,
    current_user: dict = Depends(require_admin),
) -> RestaurantRead:
    row = service.update_availability(restaurant_id, data.is_open)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant introuvable")
    return RestaurantRead(**row)