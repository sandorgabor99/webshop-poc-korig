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

# Analytics and Statistics Schemas
class AnalyticsEvent(BaseModel):
    event_type: str
    timestamp: datetime
    user_id: Optional[int] = None
    data: dict

class ProductAnalytics(BaseModel):
    product_id: int
    product_name: str
    views: int = 0
    orders: int = 0
    revenue: float = 0.0
    average_rating: float = 0.0
    review_count: int = 0
    stock_level: int = 0
    profit_margin: float = 0.0

class OrderAnalytics(BaseModel):
    total_orders: int
    total_revenue: float
    average_order_value: float
    orders_today: int
    revenue_today: float
    top_products: List[ProductAnalytics]
    sales_by_category: List[dict]
    monthly_sales: List[dict]

class UserAnalytics(BaseModel):
    total_users: int
    new_users_today: int
    active_users: int
    admin_users: int
    customer_users: int
    user_engagement: float = 0.0

class SystemStatistics(BaseModel):
    total_products: int
    total_orders: int
    total_users: int
    total_revenue: float
    average_product_rating: float
    top_selling_products: List[ProductAnalytics]
    recent_orders: List[dict]
    user_growth: dict
    sales_metrics: dict
    rating_metrics: dict

class DashboardMetrics(BaseModel):
    overview: SystemStatistics
    orders: OrderAnalytics
    users: UserAnalytics
    products: List[ProductAnalytics]
    revenue_chart: List[dict]
    orders_chart: List[dict]
    sales_analytics: dict
    rating_analytics: dict
