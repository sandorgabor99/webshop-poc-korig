import uuid
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
import enum
from .database import Base


class UserRole(enum.Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    CUSTOMER = "CUSTOMER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)  # New username field
    password_hash = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")

    @property
    def is_admin(self) -> bool:
        """Backward compatibility property for existing code"""
        return self.role == UserRole.ADMINISTRATOR


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float)
    stock = Column(Integer, default=0)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    order_items = relationship("OrderItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")

    @property
    def average_rating(self) -> float:
        """Calculate average rating for the product"""
        if not self.reviews:
            return 0.0
        total_rating = sum(review.rating for review in self.reviews)
        return round(total_rating / len(self.reviews), 1)

    @property
    def review_count(self) -> int:
        """Get the number of reviews for the product"""
        return len(self.reviews)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer)  # 1-5 stars
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True, default=lambda: f"ORD-{uuid.uuid4().hex[:8].upper()}")
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
