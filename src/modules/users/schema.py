import re

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(min_length=8, max_length=12, pattern=r"^[a-zA-Z0-9]+$")
    password: str = Field(min_length=12, max_length=64)
    role: Literal["admin", "staff", "direction"]
    restaurant_id: int | None = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not re.search(r"\d", v):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")
        return v

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    role: str
    restaurant_id: int | None

    class Config:
        from_attributes = True