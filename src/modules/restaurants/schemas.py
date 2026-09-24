from pydantic import BaseModel
from typing import Optional, Dict


class RestaurantBase(BaseModel):
    name: str
    city: str
    address: str
    is_open: bool = True
    opening_hours: Optional[Dict[str, str]] = None
    contact: Optional[Dict[str, str]] = None



class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    opening_hours: Optional[Dict[str, str]] = None
    contact: Optional[Dict[str, str]] = None


class RestaurantAvailabilityUpdate(BaseModel):
    is_open: bool


class RestaurantResponse(RestaurantBase):
    id: int

    class Config:
        from_attributes = True