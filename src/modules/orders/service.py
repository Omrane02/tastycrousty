from sqlalchemy import text

from src.db.database import engine
from src.modules.orders.schema import OrderCreate


def create_order(data: OrderCreate) -> dict:
    with engine.begin() as conn:
        restaurant = conn.execute(
            text("SELECT is_open FROM restaurants WHERE id = :id"),
            {"id": data.restaurant_id},
        ).mappings().first()

        if restaurant is None:
            raise ValueError(f"Le restaurant {data.restaurant_id} n'existe pas")
        if not restaurant["is_open"]:
            raise ValueError("Le restaurant est fermé")

        total_price = 0.0
        items_with_price = []

        for item in data.items:
            if item.quantity <= 0:
                raise ValueError("La quantité doit être supérieure à 0")

            product = conn.execute(
                text("SELECT price, restaurant_id, is_available FROM products WHERE id = :id"),
                {"id": item.product_id},
            ).mappings().first()

            if product is None:
                raise ValueError(f"Le produit {item.product_id} n'existe pas")
            if product["restaurant_id"] != data.restaurant_id:
                raise ValueError(f"Le produit {item.product_id} n'appartient pas à ce restaurant")
            if not product["is_available"]:
                raise ValueError(f"Le produit {item.product_id} est indisponible")

            unit_price = float(product["price"])
            total_price += unit_price * item.quantity
            items_with_price.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": unit_price,
            })

        order_row = conn.execute(
            text("""
                INSERT INTO orders (restaurant_id, total_price, status, pickup_mode, customer_name, customer_email)
                VALUES (:restaurant_id, :total_price, 'pending', :pickup_mode, :customer_name, :customer_email)
                RETURNING order_number, restaurant_id, created_at, total_price, status, pickup_mode, customer_name, customer_email
            """),
            {
                "restaurant_id": data.restaurant_id,
                "total_price": total_price,
                "pickup_mode": data.pickup_mode,
                "customer_name": data.customer.name,
                "customer_email": data.customer.email,
            },
        ).mappings().first()

        for item in items_with_price:
            conn.execute(
                text("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                    VALUES (:order_id, :product_id, :quantity, :unit_price)
                """),
                {"order_id": order_row["order_number"], **item},
            )

    return _build_order_dict(dict(order_row), items_with_price)


def get_order(order_number: int) -> dict | None:
    with engine.begin() as conn:
        order_row = conn.execute(
            text("SELECT * FROM orders WHERE order_number = :order_number"),
            {"order_number": order_number},
        ).mappings().first()

        if order_row is None:
            return None

        items_rows = conn.execute(
            text("SELECT product_id, quantity, unit_price FROM order_items WHERE order_id = :order_id"),
            {"order_id": order_number},
        ).mappings().all()

    return _build_order_dict(dict(order_row), [dict(row) for row in items_rows])


def list_restaurant_orders(restaurant_id: int, status_filter: str | None = None) -> list[dict]:
    query = "SELECT order_number FROM orders WHERE restaurant_id = :restaurant_id"
    params: dict = {"restaurant_id": restaurant_id}

    if status_filter is not None:
        query += " AND status = :status"
        params["status"] = status_filter

    with engine.begin() as conn:
        order_numbers = conn.execute(text(query), params).scalars().all()

    return [get_order(num) for num in order_numbers]


def update_status(order_number: int, new_status: str) -> dict | None:
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM orders WHERE order_number = :order_number"),
            {"order_number": order_number},
        ).first()
        if exists is None:
            return None

        conn.execute(
            text("UPDATE orders SET status = :status WHERE order_number = :order_number"),
            {"status": new_status, "order_number": order_number},
        )

    return get_order(order_number)


def cancel_order(order_number: int) -> dict | None:
    return update_status(order_number, "cancelled")


def _build_order_dict(order_row: dict, items: list[dict]) -> dict:
    return {
        "order_number": order_row["order_number"],
        "restaurant_id": order_row["restaurant_id"],
        "created_at": order_row["created_at"],
        "items": items,
        "total_price": float(order_row["total_price"]),
        "status": order_row["status"],
        "pickup_mode": order_row["pickup_mode"],
        "customer": {
            "name": order_row["customer_name"],
            "email": order_row["customer_email"],
        },
    }