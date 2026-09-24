from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime
from src.modules.orders.models import OrderStatus, PickupMode



class CustomerSchema(BaseModel):
    name: str
    email: EmailStr



class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="La quantité doit être supérieure à 0")



class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]
    pickup_mode: PickupMode
    customer: CustomerSchema



class OrderStatusUpdate(BaseModel):
    status: OrderStatus



class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True



class OrderResponse(BaseModel):
    order_number: str
    restaurant_id: int
    created_at: datetime
    items: List[OrderItemResponse]
    total_price: float
    status: OrderStatus
    pickup_mode: PickupMode
    customer: CustomerSchema

    class Config:
        from_attributes = True