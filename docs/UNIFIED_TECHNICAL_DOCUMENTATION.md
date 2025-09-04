# WebShop POC - Unified Technical Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Backend Implementation](#backend-implementation)
4. [Frontend Implementation](#frontend-implementation)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Testing Strategy](#testing-strategy)
7. [Infrastructure & Deployment](#infrastructure--deployment)
8. [Security & Authentication](#security--authentication)
9. [Database Design](#database-design)
10. [API Documentation](#api-documentation)
11. [Event Streaming & Analytics](#event-streaming--analytics)
12. [Kafka Setup & Configuration](#kafka-setup--configuration)
13. [Development Guidelines](#development-guidelines)
14. [Performance & Scalability](#performance--scalability)
15. [Monitoring & Observability](#monitoring--observability)
16. [Future Enhancements](#future-enhancements)

---

## Project Overview

The WebShop POC is a full-stack e-commerce application demonstrating modern software development practices, microservices architecture, and comprehensive testing strategies. The project serves as a proof-of-concept for scalable, maintainable web applications with enterprise-grade features.

### Key Features
- **Multi-role Authentication System** (Customer/Administrator)
- **Product Management** with image uploads and inventory tracking
- **Order Processing** and complete lifecycle management
- **Customer Management** with comprehensive analytics
- **Review System** with ratings and feedback
- **Real-time Analytics** and business intelligence dashboard
- **Kafka Integration** for event-driven architecture
- **Comprehensive Testing** suite with 80%+ coverage
- **CI/CD Pipeline** with automated testing and deployment
- **Security Scanning** and vulnerability detection

---

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Infrastructure│
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Docker)      │
│                 │    │                 │    │                 │
│ - User Interface│    │ - REST API      │    │ - Containers    │
│ - State Mgmt    │    │ - Business Logic│    │ - Orchestration │
│ - Analytics     │    │ - Data Access   │    │ - CI/CD         │
│ - Responsive UI │    │ - Event Stream  │    │ - Security      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Data Layer    │
                       │                 │
                       │ - SQLite/PostgreSQL
                       │ - Kafka Streams │
                       │ - File Storage  │
                       └─────────────────┘
```

### Technology Stack Overview
- **Backend**: FastAPI, Python 3.11+, SQLAlchemy, JWT
- **Frontend**: React 18, TypeScript, Vite, Chart.js
- **Database**: SQLite (dev), PostgreSQL (prod), Alembic
- **Infrastructure**: Docker, Docker Compose, GitHub Actions
- **Security**: Trivy, JWT, bcrypt, CORS
- **Testing**: Pytest, Vitest, Coverage tools
- **Event Streaming**: Apache Kafka, aioKafka

---

## Backend Implementation

### Technology Stack

#### Core Framework
- **FastAPI 0.104.1**: Modern, fast web framework for building APIs with Python 3.11+
- **Uvicorn**: ASGI server for running FastAPI applications
- **Python 3.11**: Leveraging latest Python features and performance improvements

#### Database Layer
- **SQLAlchemy 2.0.23**: Modern ORM with type safety and async support
- **Alembic 1.12.1**: Database migration management
- **SQLite** (Development) / **PostgreSQL** (Production ready)
- **Connection Pooling**: Optimized database connections

#### Authentication & Security
- **JWT (JSON Web Tokens)**: Stateless authentication with configurable expiration
- **bcrypt**: Secure password hashing with salt rounds
- **CORS Middleware**: Cross-origin resource sharing configuration
- **Role-based Access Control**: Administrator and Customer roles

#### Data Processing & Analytics
- **Pandas 2.1.4**: Data manipulation and analysis
- **NumPy 1.25.2**: Numerical computing
- **Pydantic 2.9.2**: Data validation and serialization
- **Email Validation**: RFC-compliant email verification

#### Event Streaming & Messaging
- **Apache Kafka**: Event-driven architecture support
- **aiokafka 0.11.0**: Async Kafka client for Python
- **Event Sourcing**: Audit trail and system events

#### File Handling & Media
- **Pillow 10.4.0**: Image processing and manipulation
- **Multipart File Uploads**: Secure file handling
- **Image Validation**: Format and size verification

### Architecture Patterns

#### 1. Layered Architecture
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

#### 2. Dependency Injection
- **FastAPI Dependency System**: Automatic dependency resolution
- **Database Sessions**: Context-managed database connections
- **Authentication Middleware**: JWT token validation
- **Service Layer**: Business logic separation

#### 3. Event-Driven Architecture
- **Kafka Producer**: Asynchronous event publishing
- **Event Types**: User actions, order events, system events
- **Decoupled Services**: Loose coupling between components

### Core Components

#### 1. Application Entry Point (main.py)
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

#### 2. Database Models (models.py)
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

#### 3. API Routers
- **Authentication Router**: Login, registration, token management
- **Products Router**: CRUD operations, image uploads, inventory
- **Orders Router**: Order creation, management, history
- **Users Router**: User management, profiles, statistics
- **Analytics Router**: Business intelligence, reporting
- **Customers Router**: Customer management, order history

### Performance Optimizations
- **Database Indexing**: Optimized queries and relationships
- **Async Operations**: Non-blocking I/O operations
- **Connection Pooling**: Efficient database connections
- **Caching Strategy**: Redis integration ready
- **Lazy Loading**: On-demand data fetching

---

## Frontend Implementation

### Technology Stack

#### Core Framework
- **React 18.2.0**: Modern React with concurrent features
- **TypeScript 5.2.2**: Type-safe JavaScript development
- **Vite 5.1.0**: Fast build tool and development server

#### State Management
- **React Context API**: Global state management
- **Custom Hooks**: Reusable state logic
- **Local Storage**: Persistent client-side data

#### Routing & Navigation
- **React Router DOM 6.22.0**: Client-side routing
- **Protected Routes**: Role-based access control
- **Dynamic Navigation**: Context-aware menu system

#### UI Components & Styling
- **Custom CSS Framework**: Tailwind-inspired utility classes
- **Responsive Design**: Mobile-first approach
- **Component Library**: Reusable UI components

#### Data Visualization
- **Chart.js 4.5.0**: Interactive charts and graphs
- **React Chart.js 2**: React wrapper for Chart.js
- **Google Charts**: Additional charting capabilities

#### Development Tools
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **TypeScript ESLint**: TypeScript-specific linting rules

### Architecture Patterns

#### 1. Component Architecture
```
App (Root Component)
├── Navigation (Header)
├── Routes
│   ├── Products (Public)
│   ├── ProductDetail (Public)
│   ├── Cart (Customer)
│   ├── Checkout (Customer)
│   ├── OrderHistory (Customer)
│   ├── Login/Register (Public)
│   └── Admin Routes
│       ├── ProductManagement
│       ├── OrderManagement
│       ├── CustomerManagement
│       └── Analytics
└── Context Providers
    ├── AuthContext
    └── CartContext
```

#### 2. State Management Strategy
```typescript
// Auth Context
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

// Cart Context
interface CartContextType {
  items: CartItem[];
  addItem: (product: Product, quantity: number) => void;
  removeItem: (productId: number) => void;
  clearCart: () => void;
  getTotalItems: () => number;
  getTotalPrice: () => number;
}
```

#### 3. Routing Strategy
- **Public Routes**: Products, product details, authentication
- **Protected Routes**: Customer-specific features (cart, orders)
- **Admin Routes**: Administrative functions (management, analytics)
- **Route Guards**: Authentication and role-based access control

### Core Components

#### 1. Authentication System
- **Login/Register Forms**: User authentication interface
- **Protected Routes**: Role-based access control
- **Token Management**: JWT token handling and storage
- **User Context**: Global authentication state

#### 2. Product Management
- **Product Catalog**: Grid/list view of products
- **Product Details**: Comprehensive product information
- **Image Gallery**: Product image display and management
- **Search & Filtering**: Product discovery tools

#### 3. Shopping Cart
- **Cart Management**: Add, remove, update quantities
- **Persistent Storage**: Local storage persistence
- **Real-time Updates**: Live cart calculations
- **Checkout Process**: Order completion workflow

#### 4. Order Management
- **Order History**: Customer order tracking
- **Order Details**: Comprehensive order information
- **Status Tracking**: Order lifecycle management
- **Admin Views**: Administrative order management

#### 5. Analytics Dashboard
- **Business Metrics**: Revenue, orders, users, products
- **Interactive Charts**: Trend analysis and reporting
- **Real-time Data**: Live business intelligence
- **Performance Metrics**: System and business KPIs

### Performance Optimizations
- **Code Splitting**: Lazy loading and bundle optimization
- **Image Optimization**: Responsive images and lazy loading
- **State Optimization**: Efficient state updates and rendering
- **Bundle Optimization**: Tree shaking and minification

---

## CI/CD Pipeline

### Pipeline Architecture

#### 1. Workflow Structure
```
GitHub Actions Workflow (.github/workflows/ci.yml)
├── Triggers
│   ├── Push to main/dev branches
│   ├── Pull requests to main/dev
│   └── Manual workflow dispatch
├── Jobs (Parallel & Sequential)
│   ├── test-backend (Matrix: Python 3.11, 3.12)
│   ├── test-frontend
│   ├── security-scan
│   ├── test-containers
│   ├── container-security
│   ├── build-and-push
│   ├── deploy-staging
│   ├── deploy-production
│   └── notify-deployment
└── Dependencies & Conditions
    ├── Quality Gates
    ├── Branch-specific Logic
    └── Environment Protection
```

#### 2. Job Dependencies & Flow
```
test-backend + test-frontend
       ↓
   test-containers (Build & Test Images)
       ↓
   container-security (Scan Built Images)
       ↓
   build-and-push (Tag & Push Images)
       ↓
   deploy-staging (Dev Branch) / deploy-production (Main Branch)
       ↓
   notify-deployment (Status Reporting)
```

### Key Components

#### 1. Testing Pipeline
```yaml
test-backend:
  strategy:
    matrix:
      python-version: [3.11, 3.12]
  steps:
    - Python setup with version matrix
    - Dependency installation
    - Test execution with coverage
    - Coverage reporting to Codecov
```

**Features:**
- **Matrix Testing**: Multiple Python versions
- **Coverage Reporting**: XML and HTML coverage reports
- **Codecov Integration**: Centralized coverage tracking
- **Parallel Execution**: Independent test runs

#### 2. Container Testing & Building
```yaml
test-containers:
  needs: [test-backend, test-frontend]
  steps:
    - Docker Buildx setup
    - Backend image build and test
    - Frontend image build and test
    - Docker Compose integration test
    - Image tagging for reuse
```

**Optimizations:**
- **Single Build Strategy**: Images built once, reused throughout pipeline
- **Health Checks**: Container functionality verification
- **Integration Testing**: Full-stack service testing
- **Image Reuse**: Eliminates redundant builds

#### 3. Security Scanning
```yaml
security-scan:
  permissions:
    security-events: write
  steps:
    - Trivy vulnerability scanner (source code)
    - Container image scanning
    - GitHub Security tab integration
    - SARIF format reporting
```

**Security Features:**
- **Multi-layer Scanning**: Source code and container images
- **Vulnerability Detection**: CVE identification and reporting
- **GitHub Integration**: Security tab and PR comments
- **Compliance Reporting**: SARIF format for tool integration

#### 4. Image Building & Deployment
```yaml
build-and-push:
  needs: [test-backend, test-frontend, security-scan, test-containers]
  steps:
    - Docker metadata action
    - Image tagging and pushing
    - Branch-specific image tags
    - Container registry integration
```

**Deployment Features:**
- **Branch-based Tagging**: Dev and production image versions
- **Container Registry**: GitHub Container Registry (GHCR.io)
- **Image Optimization**: Multi-stage builds and caching
- **Deployment Automation**: Staging and production environments

### Pipeline Optimizations

#### 1. Eliminated Redundancy
- **Consolidated Workflows**: Single CI workflow instead of three separate ones
- **Shared Jobs**: Common testing and building steps
- **Optimized Dependencies**: Efficient job sequencing

#### 2. Performance Improvements
- **Parallel Execution**: Independent job runs
- **Caching Strategy**: Dependency and layer caching
- **Resource Optimization**: Efficient resource utilization

#### 3. Security & Compliance
- **Access Control**: GitHub environment protection
- **Quality Gates**: Automated quality checks
- **Security Scanning**: Integrated vulnerability detection
- **Compliance Reporting**: SARIF and security tab integration

---

## Testing Strategy

### Testing Philosophy

The testing strategy follows the **Testing Pyramid** approach, emphasizing unit tests as the foundation, with integration and end-to-end tests providing additional confidence layers.

```
        /\
       /  \     E2E Tests (Few, Critical Paths)
      /____\    
     /      \   Integration Tests (API, Database)
    /________\  
   /          \ Unit Tests (Many, Fast, Isolated)
  /____________\
```

### Testing Stack

#### 1. Backend Testing
- **Pytest 7.4.3**: Primary testing framework
- **Pytest-asyncio**: Async test support
- **Pytest-cov**: Coverage reporting
- **HTTPX**: HTTP client for API testing
- **SQLAlchemy Testing**: Database testing utilities

#### 2. Frontend Testing
- **Vitest**: Fast unit testing framework
- **React Testing Library**: Component testing utilities
- **Jest DOM**: DOM testing matchers
- **User Event**: User interaction simulation
- **Coverage V8**: Code coverage reporting

#### 3. Integration Testing
- **Docker Compose**: Service integration testing
- **Health Checks**: Service availability verification
- **API Contract Testing**: Endpoint validation
- **Database Integration**: Real database testing

### Test Categories

#### 1. Unit Tests

**Backend Unit Tests**
```python
def test_user_creation():
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.role == UserRole.CUSTOMER

def test_product_average_rating():
    product = Product(name="Test Product", price=10.0)
    product.reviews = [
        Review(rating=5),
        Review(rating=3),
        Review(rating=4)
    ]
    assert product.average_rating == 4.0
    assert product.review_count == 3
```

**Frontend Unit Tests**
```typescript
describe('useCart Hook', () => {
  it('should add items to cart', () => {
    const { result } = renderHook(() => useCart());
    const product = { id: 1, name: 'Test Product', price: 10 };
    
    act(() => {
      result.current.addItem(product, 2);
    });
    
    expect(result.current.items).toHaveLength(1);
    expect(result.current.getTotalItems()).toBe(2);
  });
});
```

#### 2. Integration Tests

**API Integration Tests**
```python
def test_product_crud_operations(client, test_admin, auth_headers):
    # Create product
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 10
    }
    
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 200
    
    product_id = response.json()["id"]
    
    # Read product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
```

**Database Integration Tests**
```python
def test_order_creation_integration(db_session, test_user, test_product):
    order = Order(
        user_id=test_user.id,
        total_amount=test_product.price * 2,
        status=OrderStatus.PENDING
    )
    
    order_item = OrderItem(
        order=order,
        product_id=test_product.id,
        quantity=2,
        unit_price=test_product.price
    )
    
    db_session.add(order)
    db_session.add(order_item)
    db_session.commit()
    
    assert order.id is not None
    assert order_item.id is not None
```

#### 3. End-to-End Tests
- **Docker Compose Testing**: Full-stack service testing
- **Health Check Validation**: Service availability verification
- **API Contract Testing**: Endpoint functionality validation
- **Cross-Service Integration**: Backend-frontend communication

### Test Configuration

#### 1. Backend Configuration (pytest.ini)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

#### 2. Frontend Configuration (vitest.config.ts)
```typescript
export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    }
  }
})
```

### Coverage & Quality Metrics

#### 1. Coverage Requirements
- **Minimum Coverage**: 80% for all code
- **Coverage Reporting**: XML, HTML, and console output
- **Quality Gates**: Automated coverage checks in CI/CD
- **Trend Analysis**: Coverage tracking over time

#### 2. Quality Assurance
- **Code Standards**: PEP 8 for Python, ESLint for TypeScript
- **Static Analysis**: Type checking and linting
- **Security Scanning**: Vulnerability detection
- **Performance Testing**: Response time validation

---

## Infrastructure & Deployment

### Containerization Strategy

#### 1. Docker Images
- **Backend Image**: Python 3.11-slim with FastAPI
- **Frontend Image**: Multi-stage build with Nginx
- **Base Images**: Alpine Linux for security and size
- **Health Checks**: Container health monitoring

#### 2. Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./test.db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      backend:
        condition: service_healthy
```

### Deployment Environments

#### 1. Development Environment
- **Local Setup**: Docker Compose for development
- **Hot Reloading**: Fast development iteration
- **Database**: SQLite for simplicity
- **Services**: Backend, frontend, and optional services

#### 2. Staging Environment
- **Automated Deployment**: Dev branch triggers
- **Environment Protection**: GitHub environment rules
- **Testing**: Full test suite execution
- **Validation**: Health checks and monitoring

#### 3. Production Environment
- **Automated Deployment**: Main branch triggers
- **Environment Protection**: Approval requirements
- **Monitoring**: Comprehensive health monitoring
- **Scaling**: Production-ready infrastructure

### Container Registry Integration

#### 1. GitHub Container Registry (GHCR.io)
- **Image Storage**: Secure container image storage
- **Access Control**: Repository-based permissions
- **Versioning**: Semantic versioning and branch tagging
- **Security**: Vulnerability scanning integration

#### 2. Image Tagging Strategy
- **Latest Tags**: Development and testing images
- **Version Tags**: Semantic versioning for releases
- **Branch Tags**: Environment-specific deployments
- **Commit Tags**: Traceability and debugging

---

## Security & Authentication

### Authentication System

#### 1. JWT Implementation
- **Token Structure**: Header, payload, and signature
- **Expiration**: Configurable token lifetime
- **Refresh Tokens**: Secure token renewal
- **Stateless Design**: No server-side session storage

#### 2. Password Security
- **bcrypt Hashing**: Secure password hashing with salt
- **Salt Rounds**: Configurable security level
- **Password Validation**: Strength requirements
- **Secure Storage**: Hashed password storage only

#### 3. Role-based Access Control
- **User Roles**: Customer and Administrator
- **Permission System**: Route-level access control
- **Protected Endpoints**: Authentication requirements
- **Admin Functions**: Administrative-only features

### Security Features

#### 1. CORS Configuration
- **Cross-Origin Control**: Configurable CORS policies
- **Security Headers**: Security-focused HTTP headers
- **Origin Validation**: Allowed origin verification
- **Method Control**: HTTP method restrictions

#### 2. Input Validation
- **Pydantic Models**: Request data validation
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Input sanitization
- **File Upload Security**: File type and size validation

#### 3. Security Scanning
- **Trivy Integration**: Vulnerability detection
- **Container Security**: Image vulnerability scanning
- **Code Security**: Source code security analysis
- **Compliance Reporting**: SARIF format integration

---

## Database Design

### Data Models

#### 1. User Management
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
```

#### 2. Product Management
```python
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Numeric(10, 2))
    stock = Column(Integer, default=0)
    image_url = Column(String, nullable=True)
    category = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(timezone.utc))
```

#### 3. Order Management
```python
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Numeric(10, 2))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(timezone.utc))
```

### Database Relationships

#### 1. One-to-Many Relationships
- **User → Orders**: One user can have multiple orders
- **User → Reviews**: One user can write multiple reviews
- **Product → OrderItems**: One product can be in multiple order items
- **Product → Reviews**: One product can have multiple reviews

#### 2. Many-to-Many Relationships
- **Orders ↔ Products**: Through OrderItem junction table
- **Users ↔ Products**: Through reviews and orders

### Database Operations

#### 1. CRUD Operations
- **Create**: Product creation, user registration, order placement
- **Read**: Product catalog, user profiles, order history
- **Update**: Product updates, user profile changes, order status
- **Delete**: Product removal, user deactivation, order cancellation

#### 2. Query Optimization
- **Indexing Strategy**: Strategic database indexing
- **Eager Loading**: Relationship optimization
- **Pagination**: Large dataset handling
- **Search Optimization**: Full-text search capabilities

---

## API Documentation

### Authentication Endpoints

#### 1. User Registration
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword"
}
```

#### 2. User Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword
```

#### 3. Token Refresh
```http
POST /auth/refresh
Authorization: Bearer <refresh_token>
```

### Product Management Endpoints

#### 1. Product CRUD
```http
# List products
GET /products/?skip=0&limit=10&category=electronics

# Get product details
GET /products/{product_id}

# Create product (Admin only)
POST /products/
Authorization: Bearer <admin_token>

# Update product (Admin only)
PUT /products/{product_id}
Authorization: Bearer <admin_token>

# Delete product (Admin only)
DELETE /products/{product_id}
Authorization: Bearer <admin_token>
```

#### 2. Image Upload
```http
POST /products/{product_id}/image
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

image: <file>
```

### Order Management Endpoints

#### 1. Order Operations
```http
# Create order
POST /orders/
Authorization: Bearer <user_token>

# Get user orders
GET /orders/detailed
Authorization: Bearer <user_token>

# Get order summary
GET /orders/summary
Authorization: Bearer <user_token>

# Get specific order
GET /orders/{order_id}
Authorization: Bearer <user_token>
```

#### 2. Admin Order Management
```http
# List all orders (Admin only)
GET /orders/admin/all?skip=0&limit=20
Authorization: Bearer <admin_token>

# Get customer orders (Admin only)
GET /orders/admin/customer/{user_id}
Authorization: Bearer <admin_token>
```

### Customer Management Endpoints

#### 1. Customer Operations
```http
# List customers (Admin only)
GET /customers/?skip=0&limit=20
Authorization: Bearer <admin_token>

# Get customer details (Admin only)
GET /customers/{user_id}
Authorization: Bearer <admin_token>

# Get customer summary (Admin only)
GET /customers/{user_id}/summary
Authorization: Bearer <admin_token>
```

### Analytics Endpoints

#### 1. Business Intelligence
```http
# Get overview statistics
GET /analytics/overview
Authorization: Bearer <admin_token>

# Get revenue trends
GET /analytics/revenue?days=30
Authorization: Bearer <admin_token>

# Get order trends
GET /analytics/orders?days=30
Authorization: Bearer <admin_token>

# Get user growth
GET /analytics/users?days=7
Authorization: Bearer <admin_token>
```

---

## Event Streaming & Analytics

### Kafka Integration

#### 1. Event Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Kafka         │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Broker)      │
│                 │    │                 │    │                 │
│ - Statistics    │    │ - Analytics     │    │ - Event Topics  │
│   Dashboard     │    │   Router        │    │ - Streams       │
│ - Charts        │    │ - Kafka         │    │ - Consumers     │
│ - Metrics       │    │   Producer      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### 2. Event Types
- **Product Events**: `product_viewed`, `product_created`, `product_updated`, `product_deleted`
- **Order Events**: `order_created`, `order_completed`
- **User Events**: `user_registered`, `user_login`, `admin_dashboard_access`
- **Analytics Events**: `product_list_viewed`, `cart_updated`

#### 3. Event Schema
```json
{
  "event_type": "product_viewed",
  "timestamp": "2024-01-01T12:00:00Z",
  "user_id": 123,
  "data": {
    "product_id": 456,
    "product_name": "Sample Product",
    "price": 29.99,
    "category": "electronics"
  }
}
```

#### 4. Kafka Topics
- **`webshop-analytics`**: Main analytics events topic
- **`webshop-products`**: Product-related events
- **`webshop-orders`**: Order-related events
- **`webshop-users`**: User-related events

#### 5. Event Tracking Implementation
```python
# Product Events
await kafka.send_product_event("product_viewed", product_data)
await kafka.send_product_event("product_created", product_data, admin_user_id)
await kafka.send_product_event("product_updated", product_data, admin_user_id)

# Order Events
await kafka.send_order_event("order_created", order_data, user_id)
await kafka.send_order_event("order_completed", order_data, user_id)

# User Events
await kafka.send_user_event("user_registered", user_data, user_id)
await kafka.send_user_event("admin_dashboard_access", user_data, user_id)
```

### Analytics Dashboard

#### 1. Overview Tab
- Total revenue, orders, users, and products
- Revenue trend chart (last 30 days)
- Orders trend chart (last 30 days)
- Recent orders table

#### 2. Orders Tab
- Order statistics and metrics
- Today's orders and revenue
- Top selling products
- Average order value

#### 3. Users Tab
- User growth analytics
- Active user metrics
- Role-based user counts
- User growth chart (last 7 days)

#### 4. Products Tab
- Product performance metrics
- Order counts and revenue per product
- Rating and review analytics
- Performance comparison

### Real-time Features
- **Live Updates**: Real-time dashboard updates
- **Event Streaming**: Continuous data flow
- **Performance Metrics**: Live system monitoring
- **Business Intelligence**: Real-time analytics

### Performance Considerations
- **Event Batching**: Events are sent asynchronously with non-blocking transmission
- **Database Optimization**: Analytics queries use database indexes and cached calculations
- **Frontend Performance**: Lazy loading of chart data and optimized re-renders
- **Graceful Fallback**: System continues to function if Kafka is unavailable

---

## Kafka Setup & Configuration

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ with required dependencies
- Node.js 18+ for frontend

### Environment Configuration
```bash
# Copy environment file
cp env.example .env

# Edit .env file with Kafka settings
KAFKA_ENABLED=true
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_ANALYTICS_TOPIC=webshop-analytics
KAFKA_PRODUCTS_TOPIC=webshop-products
KAFKA_ORDERS_TOPIC=webshop-orders
KAFKA_USERS_TOPIC=webshop-users
```

### Starting Kafka Services
```bash
# Start Kafka, Zookeeper, and Kafka UI
docker-compose -f docker-compose.kafka.yml up -d

# Verify services are running
docker-compose -f docker-compose.kafka.yml ps

# Check Kafka UI at http://localhost:8080
```

### API Endpoints

#### Analytics Endpoints
| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/analytics/dashboard` | GET | Complete dashboard metrics | Admin |
| `/analytics/overview` | GET | System overview statistics | Admin |
| `/analytics/orders` | GET | Order analytics | Admin |
| `/analytics/users` | GET | User analytics | Admin |
| `/analytics/products` | GET | Product analytics | Admin |

### Monitoring & Debugging

#### Kafka UI
Access the Kafka UI at `http://localhost:8080` to:
- View topics and messages
- Monitor consumer groups
- Inspect message content
- Manage topics

#### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Kafka connectivity
curl http://localhost:8000/analytics/dashboard
```

#### Logs
```bash
# Backend logs
tail -f logs/app.log

# Kafka logs
docker-compose -f docker-compose.kafka.yml logs -f kafka
```

### Troubleshooting

#### Common Issues
1. **Kafka Connection Failed**
   ```bash
   # Check if Kafka is running
   docker-compose -f docker-compose.kafka.yml ps
   
   # Restart Kafka services
   docker-compose -f docker-compose.kafka.yml restart
   ```

2. **Analytics Dashboard Not Loading**
   - Verify backend is running
   - Check authentication token
   - Review browser console for errors

3. **Events Not Being Sent**
   - Check Kafka connectivity
   - Verify topic exists
   - Review backend logs

#### Debug Mode
```python
# Enable debug logging in config.py
KAFKA_DEBUG = True
```

### Security Considerations
- **Access Control**: All analytics endpoints require admin authentication
- **Data Privacy**: User IDs are anonymized in analytics events
- **JWT Validation**: Secure token validation for all endpoints
- **GDPR Compliance**: Sensitive data is not logged

---

## Development Guidelines

### Code Standards

#### 1. Python Standards
- **PEP 8**: Python style guide compliance
- **Type Hints**: Comprehensive type annotations
- **Docstrings**: Clear function documentation
- **Error Handling**: Proper exception management

#### 2. TypeScript Standards
- **ESLint**: Code quality enforcement
- **Prettier**: Code formatting consistency
- **Type Safety**: Strict TypeScript configuration
- **Component Standards**: React best practices

### Testing Requirements

#### 1. Coverage Standards
- **Minimum Coverage**: 80% for all code
- **Test Categories**: Unit, integration, and E2E tests
- **Quality Gates**: Automated quality checks
- **Performance Testing**: Response time validation

#### 2. Test Writing Guidelines
- **Test Naming**: Clear, descriptive test names
- **Test Structure**: Arrange, Act, Assert pattern
- **Mocking Strategy**: Appropriate test isolation
- **Data Management**: Test data setup and cleanup

### Security Guidelines

#### 1. Authentication
- **JWT Best Practices**: Secure token handling
- **Password Security**: Strong password requirements
- **Access Control**: Role-based permissions
- **Session Management**: Secure session handling

#### 2. Data Protection
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Output encoding
- **File Upload Security**: Secure file handling

---

## Performance & Scalability

### Performance Optimizations

#### 1. Database Optimization
- **Indexing Strategy**: Strategic database indexing
- **Query Optimization**: Efficient SQL queries
- **Connection Pooling**: Optimized database connections
- **Caching Strategy**: Redis integration ready

#### 2. Frontend Optimization
- **Code Splitting**: Lazy loading and bundle optimization
- **Image Optimization**: Responsive images and lazy loading
- **State Optimization**: Efficient state updates
- **Bundle Optimization**: Tree shaking and minification

#### 3. Backend Optimization
- **Async Operations**: Non-blocking I/O operations
- **Caching Layers**: Multi-level caching strategy
- **Database Optimization**: Query performance tuning
- **Resource Management**: Efficient resource utilization

### Scalability Features

#### 1. Microservices Architecture
- **Service Decoupling**: Independent service deployment
- **API Gateway**: Centralized request routing
- **Load Balancing**: Distributed request handling
- **Service Discovery**: Dynamic service location

#### 2. Event-Driven Architecture
- **Kafka Integration**: Scalable event streaming
- **Asynchronous Processing**: Non-blocking operations
- **Event Sourcing**: Audit trail and system events
- **Decoupled Services**: Loose coupling between components

#### 3. Container Orchestration
- **Docker Ready**: Containerized deployment
- **Kubernetes Ready**: Production orchestration
- **Auto-scaling**: Dynamic resource allocation
- **Health Monitoring**: Comprehensive health checks

---

## Monitoring & Observability

### Health Monitoring

#### 1. Service Health Checks
- **Backend Health**: `/health` endpoint monitoring
- **Frontend Health**: Container health verification
- **Database Health**: Connection status monitoring
- **External Services**: Kafka and other service health

#### 2. Container Health
- **Docker Health Checks**: Container functionality verification
- **Service Availability**: Service response validation
- **Resource Monitoring**: CPU, memory, and disk usage
- **Network Connectivity**: Service communication verification

### Performance Monitoring

#### 1. Application Metrics
- **Response Times**: API endpoint performance
- **Throughput**: Request handling capacity
- **Error Rates**: Error frequency and patterns
- **Resource Usage**: System resource utilization

#### 2. Business Metrics
- **Revenue Tracking**: Sales and revenue monitoring
- **Order Metrics**: Order processing performance
- **User Activity**: User engagement and behavior
- **Product Performance**: Product popularity and sales

### Logging & Debugging

#### 1. Log Management
- **Structured Logging**: JSON format logging
- **Log Levels**: Appropriate log level usage
- **Error Tracking**: Comprehensive error logging
- **Audit Trails**: User action tracking

#### 2. Debugging Tools
- **Development Mode**: Enhanced debugging information
- **Error Reporting**: Detailed error information
- **Performance Profiling**: Performance analysis tools
- **Database Query Logging**: SQL query monitoring

---

## Future Enhancements

### Planned Features

#### 1. Multi-tenancy
- **Store Management**: Multiple store support
- **Tenant Isolation**: Data separation and security
- **Customization**: Store-specific configurations
- **Scalability**: Multi-tenant architecture

#### 2. Payment Integration
- **Stripe Integration**: Credit card processing
- **Payment Methods**: Multiple payment options
- **Subscription Support**: Recurring billing
- **Payment Security**: PCI compliance

#### 3. Advanced Analytics
- **Machine Learning**: Predictive analytics
- **Business Intelligence**: Advanced reporting
- **Data Visualization**: Interactive dashboards
- **Performance Insights**: System optimization

#### 4. Mobile Application
- **React Native**: Cross-platform mobile app
- **Offline Support**: Offline functionality
- **Push Notifications**: Real-time updates
- **Mobile Optimization**: Mobile-specific features

### Technical Improvements

#### 1. API Enhancements
- **GraphQL API**: Alternative to REST API
- **Real-time Updates**: WebSocket integration
- **API Versioning**: Backward compatibility
- **Rate Limiting**: API usage control

#### 2. Infrastructure Improvements
- **Advanced Caching**: Redis cluster and CDN integration
- **Load Balancing**: Advanced load balancing strategies
- **Auto-scaling**: Dynamic resource allocation
- **Disaster Recovery**: Backup and recovery strategies

#### 3. Security Enhancements
- **Advanced Authentication**: Multi-factor authentication
- **API Security**: Advanced API protection
- **Compliance**: GDPR and other compliance requirements
- **Security Monitoring**: Advanced threat detection

#### 4. Kafka & Event Streaming Improvements
- **Real-time Dashboard Updates**: WebSocket integration for live analytics
- **Advanced Charting**: Enhanced visualizations with Chart.js or D3.js
- **Data Export**: CSV/Excel export functionality for analytics data
- **Email Reports**: Automated reporting and alerting system
- **Custom Date Filtering**: Advanced time-based analytics
- **Predictive Analytics**: Machine learning insights
- **Scalability**: Redis caching, multiple consumers, horizontal scaling
- **Data Retention**: Configurable data retention policies

---

## Quick Start Guide

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Local Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd webshop-poc

# Backend setup
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install

# Start services
docker-compose up -d
```

### Running Tests
```bash
# Backend tests
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose up -d
# Wait for services to be ready
curl -f http://localhost:8000/health
curl -f http://localhost:80/health
```

### Accessing the Application
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:80
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Support & Contributing

### Getting Help
- **Documentation**: Comprehensive technical documentation
- **Code Examples**: Working examples and test cases
- **API Reference**: Complete API endpoint documentation
- **Issue Tracking**: GitHub issues for bug reports and feature requests

### Contributing
- **Code Standards**: PEP 8 for Python, ESLint for TypeScript
- **Testing Requirements**: Comprehensive test coverage
- **Security Review**: Security scanning and vulnerability assessment
- **Documentation**: Keep documentation up to date

---

**Last Updated**: September 2025  
**Version**: 1.0.0  
**Maintainer**: SG  
**Documentation Status**: Unified and Consolidated
