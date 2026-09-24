from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.db.database import engine
from src.core.security import hash_password
from src.modules.users.schema import UserCreate


def create_user(data: UserCreate) -> dict:
    hashed = hash_password(data.password)

    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM users WHERE username = :username"),
            {"username": data.username},
        ).first()
        if exists:
            raise ValueError("Ce nom d'utilisateur existe déjà")

        if data.restaurant_id is not None:
            restaurant_exists = conn.execute(
                text("SELECT 1 FROM restaurants WHERE id = :restaurant_id"),
                {"restaurant_id": data.restaurant_id},
            ).first()
            if not restaurant_exists:
                raise ValueError(f"Le restaurant {data.restaurant_id} n'existe pas")

        result = conn.execute(
            text("""
                INSERT INTO users (first_name, last_name, username, hashed_password, role, restaurant_id)
                VALUES (:first_name, :last_name, :username, :hashed_password, :role, :restaurant_id)
                RETURNING id, first_name, last_name, username, role, restaurant_id
            """),
            {
                "first_name": data.first_name,
                "last_name": data.last_name,
                "username": data.username,
                "hashed_password": hashed,
                "role": data.role,
                "restaurant_id": data.restaurant_id,
            },
        )
        row = result.mappings().first()

    return dict(row)