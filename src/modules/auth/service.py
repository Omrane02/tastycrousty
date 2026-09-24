from sqlalchemy import text

from src.db.database import engine
from src.core.security import verify_password


def authenticate_user(username: str, password: str) -> dict | None:
    with engine.begin() as conn:
        row = conn.execute(
            text("""
                SELECT id, username, hashed_password, role, restaurant_id
                FROM users
                WHERE username = :username
            """),
            {'username': username}
        ).mappings().first()

    if row is None:
        return None
    if not verify_password(password, row["hashed_password"]):
        return None

    return dict(row)