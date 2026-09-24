from pydantic import BaseModel, Field
from typing import Optional, List



class ProductBase(BaseModel):
    name: str
    image: Optional[str] = None
    description: Optional[str] = None
    category: str
    price: float = Field(..., gt=0)
    is_available: bool = True
    restaurant_id: int
    ingredients: Optional[List[str]] = []



class ProductCreate(ProductBase):
    pass



class ProductUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    restaurant_id: Optional[int] = None
    ingredients: Optional[List[str]] = None



class ProductAvailabilityUpdate(BaseModel):
    is_available: bool



class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True