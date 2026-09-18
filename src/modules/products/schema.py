from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    image: str
    description: str
    category: str
    price: float= Field(gt= 0)
    is_available: bool
    restaurant_id: int
    ingredients: list [str]

class ProductRead(BaseModel):
    id : int
    name: str
    image: str
    description: str
    category: str
    price: float
    is_available: bool
    ingredients: list [str]
    restaurant_id: int

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str | None = None
    image: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = Field(default=None, gt=0)
    restaurant_id: int | None = None
    ingredients: list[str] | None = None


class ProductAvailabilityUpdate(BaseModel):
    is_available: bool