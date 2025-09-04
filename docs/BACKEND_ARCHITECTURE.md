# Backend Architecture Documentation

## Technology Stack

### Core Framework
- **FastAPI 0.104.1**: Modern, fast web framework for building APIs with Python 3.11+
- **Uvicorn**: ASGI server for running FastAPI applications
- **Python 3.11**: Leveraging latest Python features and performance improvements

### Database Layer
- **SQLAlchemy 2.0.23**: Modern ORM with type safety and async support
- **Alembic 1.12.1**: Database migration management
- **SQLite** (Development) / **PostgreSQL** (Production ready)
- **Connection Pooling**: Optimized database connections

### Authentication & Security
- **JWT (JSON Web Tokens)**: Stateless authentication with configurable expiration
- **bcrypt**: Secure password hashing with salt rounds
- **CORS Middleware**: Cross-origin resource sharing configuration
- **Role-based Access Control**: Administrator and Customer roles

### Data Processing & Analytics
- **Pandas 2.1.4**: Data manipulation and analysis
- **NumPy 1.25.2**: Numerical computing
- **Pydantic 2.9.2**: Data validation and serialization
- **Email Validation**: RFC-compliant email verification

### Event Streaming & Messaging
- **Apache Kafka**: Event-driven architecture support
- **aiokafka 0.11.0**: Async Kafka client for Python
- **Event Sourcing**: Audit trail and system events

### File Handling & Media
- **Pillow 10.4.0**: Image processing and manipulation
- **Multipart File Uploads**: Secure file handling
- **Image Validation**: Format and size verification

## Architecture Patterns

### 1. Layered Architecture
```
┌─────────────────────────────────────┐
│           API Layer                 │
│        (FastAPI Routes)            │
├─────────────────────────────────────┤
│         Business Logic              │
│      (Service Layer)               │
├─────────────────────────────────────┤
│         Data Access Layer          │
│      (SQLAlchemy Models)           │
├─────────────────────────────────────┤
│         Database Layer              │
│      (SQLite/PostgreSQL)           │
└─────────────────────────────────────┘
```

### 2. Dependency Injection
- **FastAPI Dependency System**: Automatic dependency resolution
- **Database Sessions**: Context-managed database connections
- **Authentication Middleware**: JWT token validation
- **Service Layer**: Business logic separation

### 3. Event-Driven Architecture
- **Kafka Producer**: Asynchronous event publishing
- **Event Types**: User actions, order events, system events
- **Decoupled Services**: Loose coupling between components

## Core Components

### 1. Application Entry Point (main.py)
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Database initialization, admin seeding, Kafka setup
    # Shutdown: Cleanup connections, graceful shutdown
```

**Key Responsibilities:**
- Application lifecycle management
- Database schema initialization
- Admin user seeding
- Kafka producer initialization
- Graceful shutdown handling

### 2. Database Models (models.py)
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
```

**Model Relationships:**
- **User ↔ Order**: One-to-many relationship
- **User ↔ Review**: One-to-many relationship
- **Product ↔ OrderItem**: One-to-many relationship
- **Product ↔ Review**: One-to-many relationship
- **Order ↔ OrderItem**: One-to-many relationship

### 3. Router Modules
- **auth.py**: Authentication endpoints (login, register, token refresh)
- **products.py**: Product CRUD operations and search
- **orders.py**: Order management and processing
- **customers.py**: Customer data management
- **reviews.py**: Review system and ratings
- **analytics.py**: Business intelligence and reporting
- **upload.py**: File upload and image management

### 4. Security Implementation
```python
class SecurityConfig:
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Password hashing
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # JWT token creation
    def create_access_token(data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

## Performance Optimizations

### 1. Database Optimization
- **Indexed Fields**: Primary keys, foreign keys, search fields
- **Connection Pooling**: Efficient database connection management
- **Lazy Loading**: On-demand relationship loading
- **Query Optimization**: Efficient SQL generation

### 2. Caching Strategy
- **Redis Integration**: Ready for session and data caching
- **Response Caching**: FastAPI response caching middleware
- **Database Query Caching**: Frequently accessed data caching

### 3. Async Operations
- **FastAPI Async Support**: Non-blocking request handling
- **Kafka Async Client**: Non-blocking message publishing
- **Database Async Operations**: Concurrent database access

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Token refresh
- `GET /auth/me` - Current user info

### Products
- `GET /products/` - List products
- `POST /products/` - Create product (admin)
- `GET /products/{id}` - Get product
- `PUT /products/{id}` - Update product (admin)
- `DELETE /products/{id}` - Delete product (admin)

### Orders
- `GET /orders/` - List user orders
- `POST /orders/` - Create order
- `GET /orders/{id}` - Get order details
- `PUT /orders/{id}` - Update order (admin)

### Analytics
- `GET /analytics/sales` - Sales analytics
- `GET /analytics/orders` - Order analytics
- `GET /analytics/customers` - Customer analytics
- `GET /analytics/products` - Product analytics
