from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemRead(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class CustomerInfo(BaseModel):
    name: str
    email: str

class OrderCreate(BaseModel):
    restaurant_id: int
    items: list[OrderItemCreate]
    pickup_mode: Literal["onsite","takeaway"]
    customer: CustomerInfo

class OrderRead(BaseModel):
    order_number: int
    restaurant_id: int
    created_at: datetime
    items: list[OrderItemRead]
    total_price: float=Field(gt=0)
    status: Literal["pending","validated","preparing","ready","collected","cancelled"]
    pickup_mode: Literal["onsite","takeaway"]
    customer:CustomerInfo

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: Literal["pending","validated","preparing","ready","collected"]




