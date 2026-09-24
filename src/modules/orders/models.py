import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship


from sqlalchemy.orm import declarative_base
Base = declarative_base()


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    PREPARING = "preparing"
    READY = "ready"
    COLLECTED = "collected"
    CANCELLED = "cancelled"


class PickupMode(str, enum.Enum):
    ONSITE = "onsite"
    TAKEAWAY = "takeaway"


class Order(Base):
    __tablename__ = "orders"

    order_number = Column(String, primary_key=True, index=True)
    restaurant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    pickup_mode = Column(Enum(PickupMode), nullable=False)

    
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)

    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_number = Column(String, ForeignKey("orders.order_number"), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")