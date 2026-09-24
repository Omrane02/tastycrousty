from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session


from src.modules.orders.models import Order, OrderStatus
from src.modules.orders.schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)
from src.modules.orders.service import create_order_logic

router = APIRouter(prefix="/orders", tags=["Orders"])



@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    return create_order_logic(db, order_in)



@router.get("/{order_number}", response_model=OrderResponse)
def get_order_by_number(order_number: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commande introuvable.",
        )
    return order



@router.get("/restaurant/{restaurant_id}", response_model=List[OrderResponse])
def get_restaurant_orders(
    restaurant_id: int,
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    
):
    query = db.query(Order).filter(Order.restaurant_id == restaurant_id)
    if status_filter:
        query = query.filter(Order.status == status_filter)
    return query.all()



@router.patch("/{order_number}/status", response_model=OrderResponse)
def update_order_status(
    order_number: str,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    
):
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commande introuvable.",
        )

    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order



@router.post("/{order_number}/cancel", response_model=OrderResponse)
def cancel_order(
    order_number: str,
    db: Session = Depends(get_db),
    
):
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commande introuvable.",
        )

    order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(order)
    return order