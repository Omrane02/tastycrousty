from pydantic import BaseModel

class RestaurantRead(BaseModel):
    id : int
    name: str
    city : str
    address : str | None
    is_open: bool
    opening_hours : str | None
    contact: str | None

    class Config:
        from_attributes = True

class RestaurantUpdate(BaseModel):
    name : str | None = None
    city : str | None = None
    address : str | None = None
    opening_hours : str | None = None
    contact: str | None = None

class RestaurantAvailabilityUpdate(BaseModel):
    is_open : bool