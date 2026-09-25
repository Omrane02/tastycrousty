from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import check_order_restaurant_access, get_current_user
from src.modules.orders import service
from src.modules.orders.schema import OrderCreate, OrderRead, OrderStatusUpdate

router = APIRouter(tags=["orders"])


@router.post("/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate) -> OrderRead:
    try:
        order = service.create_order(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return OrderRead(**order)


@router.get("/orders/{order_number}", response_model=OrderRead)
def get_order(order_number: int) -> OrderRead:
    order = service.get_order(order_number)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")
    return OrderRead(**order)


@router.get("/restaurants/{restaurant_id}/orders", response_model=list[OrderRead])
def list_restaurant_orders(
    restaurant_id: int,
    status: str | None = None,
    current_user: dict = Depends(get_current_user),
) -> list[OrderRead]:
    check_order_restaurant_access(current_user, restaurant_id)
    orders = service.list_restaurant_orders(restaurant_id, status)
    return [OrderRead(**o) for o in orders]


@router.patch("/orders/{order_number}/status", response_model=OrderRead)
def update_order_status(
    order_number: int,
    data: OrderStatusUpdate,
    current_user: dict = Depends(get_current_user),
) -> OrderRead:
    existing = service.get_order(order_number)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")

    check_order_restaurant_access(current_user, existing["restaurant_id"])

    order = service.update_status(order_number, data.status)
    return OrderRead(**order)


@router.post("/orders/{order_number}/cancel", response_model=OrderRead)
def cancel_order(
    order_number: int,
    current_user: dict = Depends(get_current_user),
) -> OrderRead:
    existing = service.get_order(order_number)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commande introuvable")

    check_order_restaurant_access(current_user, existing["restaurant_id"])

    order = service.cancel_order(order_number)
    return OrderRead(**order)