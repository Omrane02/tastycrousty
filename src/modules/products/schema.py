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