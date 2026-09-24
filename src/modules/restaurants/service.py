from sqlalchemy import text

from src.db.database import engine
from src.modules.restaurants.schema import RestaurantUpdate


def get_all_restaurants() -> list[dict]:
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT * FROM restaurants ORDER BY id")).mappings().all()
    return [dict(row) for row in rows]


def get_restaurant(restaurant_id: int) -> dict | None:
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT * FROM restaurants WHERE id = :id"),
            {"id": restaurant_id},
        ).mappings().first()
    return dict(row) if row else None


def update_restaurant(restaurant_id: int, data: RestaurantUpdate) -> dict | None:
    fields = data.model_dump(exclude_unset=True)
    if not fields:
        return get_restaurant(restaurant_id)

    set_clause = ", ".join(f"{key} = :{key}" for key in fields)
    fields["id"] = restaurant_id

    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM restaurants WHERE id = :id"), {"id": restaurant_id}
        ).first()
        if not exists:
            return None

        conn.execute(text(f"UPDATE restaurants SET {set_clause} WHERE id = :id"), fields)
        row = conn.execute(
            text("SELECT * FROM restaurants WHERE id = :id"), {"id": restaurant_id}
        ).mappings().first()

    return dict(row)


def update_availability(restaurant_id: int, is_open: bool) -> dict | None:
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM restaurants WHERE id = :id"), {"id": restaurant_id}
        ).first()
        if not exists:
            return None

        conn.execute(
            text("UPDATE restaurants SET is_open = :is_open WHERE id = :id"),
            {"is_open": is_open, "id": restaurant_id},
        )
        row = conn.execute(
            text("SELECT * FROM restaurants WHERE id = :id"), {"id": restaurant_id}
        ).mappings().first()

    return dict(row)