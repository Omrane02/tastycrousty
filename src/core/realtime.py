import socketio

# cors_allowed_origins="*" : le socket ne transporte que des numéros de commande et des statuts.
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


def restaurant_room(restaurant_id: int) -> str:
    return f"restaurant:{restaurant_id}"


@sio.event
async def join_restaurant(sid: str, data: dict) -> None:
    """La cuisine d'un restaurant rejoint sa salle pour recevoir ses événements."""
    restaurant_id = data.get("restaurant_id") if isinstance(data, dict) else None
    if isinstance(restaurant_id, int):
        await sio.enter_room(sid, restaurant_room(restaurant_id))


@sio.event
async def leave_restaurant(sid: str, data: dict) -> None:
    restaurant_id = data.get("restaurant_id") if isinstance(data, dict) else None
    if isinstance(restaurant_id, int):
        await sio.leave_room(sid, restaurant_room(restaurant_id))


async def emit_order_event(event: str, restaurant_id: int, order_number: int, order_status: str) -> None:
    """Prévient l'écran cuisine du restaurant concerné (le front recharge ensuite via l'API REST)."""
    await sio.emit(
        event,
        {"order_number": order_number, "restaurant_id": restaurant_id, "status": order_status},
        room=restaurant_room(restaurant_id),
    )