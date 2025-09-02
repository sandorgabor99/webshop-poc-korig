from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    CUSTOMER = "CUSTOMER"


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50, description="Username must be 3-50 characters")


class UserCreate(UserBase):
    password: str = Field(min_length=6)
    role: Optional[UserRole] = UserRole.CUSTOMER


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    @computed_field
    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMINISTRATOR


class UserWithOrders(UserOut):
    """User information with their order count"""
    order_count: int
    total_spent: float


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None


class Product(ProductBase):
    id: int
    created_at: datetime
    average_rating: float
    review_count: int

    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    rating: int = Field(ge=1, le=5, description="Rating from 1 to 5 stars")
    feedback: Optional[str] = Field(None, max_length=1000, description="Optional feedback text")


class ReviewCreate(ReviewBase):
    product_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = Field(None, max_length=1000)


class ReviewOut(ReviewBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    user: UserOut

    model_config = ConfigDict(from_attributes=True)


class ProductWithReviews(Product):
    """Product with detailed review information"""
    reviews: List[ReviewOut]


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderItemWithProduct(OrderItemOut):
    """Order item with product details"""
    product: Product


class OrderOut(BaseModel):
    id: int
    order_id: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)


class OrderWithDetails(OrderOut):
    """Order with detailed item information including products"""
    items: List[OrderItemWithProduct]
    user: UserOut


class CustomerOrderSummary(BaseModel):
    """Summary of customer's order history"""
    total_orders: int
    total_spent: float
    average_order_value: float
    last_order_date: Optional[datetime]
