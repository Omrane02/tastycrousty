from sqlalchemy import text

from src.db.database import engine
from src.modules.products.schema import ProductCreate, ProductUpdate


def list_products(
    category: str | None = None,
    q: str | None = None,
    restaurant_id: int | None = None,
    is_available: bool | None = None,
) -> list[dict]:
    conditions = []
    params: dict = {}

    if category is not None:
        conditions.append("category = :category")
        params["category"] = category
    if q is not None:
        conditions.append("""
            (
                name ILIKE :q
                OR description ILIKE :q
                OR category ILIKE :q
                OR array_to_string(ingredients, ' ') ILIKE :q
            )
        """)
        params["q"] = f"%{q}%"
    if restaurant_id is not None:
        conditions.append("restaurant_id = :restaurant_id")
        params["restaurant_id"] = restaurant_id
    if is_available is not None:
        conditions.append("is_available = :is_available")
        params["is_available"] = is_available

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    with engine.begin() as conn:
        rows = conn.execute(
            text(f"SELECT * FROM products {where_clause} ORDER BY id"), params
        ).mappings().all()

    return [dict(row) for row in rows]


def get_product(product_id: int) -> dict | None:
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT * FROM products WHERE id = :id"), {"id": product_id}
        ).mappings().first()
    return dict(row) if row else None


def create_product(data: ProductCreate) -> dict:
    with engine.begin() as conn:
        restaurant_exists = conn.execute(
            text("SELECT 1 FROM restaurants WHERE id = :id"), {"id": data.restaurant_id}
        ).first()
        if not restaurant_exists:
            raise ValueError(f"Le restaurant {data.restaurant_id} n'existe pas")

        result = conn.execute(
            text("""
                INSERT INTO products (name, image, description, category, price, is_available, restaurant_id, ingredients)
                VALUES (:name, :image, :description, :category, :price, :is_available, :restaurant_id, :ingredients)
                RETURNING *
            """),
            data.model_dump(),
        )
        row = result.mappings().first()

    return dict(row)


def update_product(product_id: int, data: ProductUpdate) -> dict | None:
    fields = data.model_dump(exclude_unset=True)

    with engine.begin() as conn:
        existing = conn.execute(
            text("SELECT * FROM products WHERE id = :id"), {"id": product_id}
        ).mappings().first()
        if existing is None:
            return None

        if not fields:
            return dict(existing)

        set_clause = ", ".join(f"{key} = :{key}" for key in fields)
        fields["id"] = product_id
        conn.execute(text(f"UPDATE products SET {set_clause} WHERE id = :id"), fields)

        row = conn.execute(
            text("SELECT * FROM products WHERE id = :id"), {"id": product_id}
        ).mappings().first()

    return dict(row)


def update_availability(product_id: int, is_available: bool) -> dict | None:
    with engine.begin() as conn:
        existing = conn.execute(
            text("SELECT 1 FROM products WHERE id = :id"), {"id": product_id}
        ).first()
        if existing is None:
            return None

        conn.execute(
            text("UPDATE products SET is_available = :is_available WHERE id = :id"),
            {"is_available": is_available, "id": product_id},
        )
        row = conn.execute(
            text("SELECT * FROM products WHERE id = :id"), {"id": product_id}
        ).mappings().first()

    return dict(row)


def delete_product(product_id: int) -> dict | None:
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT * FROM products WHERE id = :id"), {"id": product_id}
        ).mappings().first()
        if row is None:
            return None

        conn.execute(text("DELETE FROM products WHERE id = :id"), {"id": product_id})

    return dict(row)