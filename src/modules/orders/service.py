import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.modules.orders.models import Order, OrderItem, OrderStatus
from src.modules.orders.schemas import OrderCreate




def create_order_logic(db: Session, order_in: OrderCreate):
    
    restaurant = db.query(Restaurant).filter(Restaurant.id == order_in.restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le restaurant n'existe pas."
        )
    if not restaurant.is_open:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le restaurant est actuellement fermé."
        )

    total_price = 0.0
    items_to_create = []

    
    for item in order_in.items:
        if item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La quantité doit être supérieure à 0."
            )

        
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le produit {item.product_id} n'existe pas."
            )

        if product.restaurant_id != order_in.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le produit {product.name} n'appartient pas à ce restaurant."
            )

        if not product.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le produit {product.name} est indisponible."
            )

        
        total_price += product.price * item.quantity

        items_to_create.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity
            )
        )

    
    generated_order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

   
    new_order = Order(
        order_number=generated_order_number,
        restaurant_id=order_in.restaurant_id,
        total_price=round(total_price, 2),
        pickup_mode=order_in.pickup_mode,
        status=OrderStatus.PENDING,
        customer_name=order_in.customer.name,
        customer_email=order_in.customer.email,
        items=items_to_create
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order