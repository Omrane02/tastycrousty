from sqlalchemy import text

from src.db.database import engine
from src.core.security import hash_password


def seed_data() -> None:
    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM restaurants")).scalar()
        if count == 0:
            conn.execute(text("""
                INSERT INTO restaurants (name, city, is_open)
                VALUES
                ('Ytasty Crousty Aix', 'Aix', true),
                ('Ytasty Crousty Lyon', 'Lyon', true),
                ('Ytasty Crousty Paris', 'Paris', true)
            """))

        exists = conn.execute(
            text("SELECT 1 FROM users WHERE username = :u"),
            {"u": "admin123"},
        ).first()

        if not exists:
            hashed = hash_password("Admin@123456")
            conn.execute(
                text("""
                    INSERT INTO users (first_name, last_name, username, hashed_password, role)
                    VALUES ('Admin', 'Admin', :username, :hashed_password, 'admin')
                """),
                {"username": "admin123", "hashed_password": hashed},
            )