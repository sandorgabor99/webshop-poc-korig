# WebShop POC

A full-stack e-commerce proof of concept with FastAPI backend and React frontend, featuring real-time analytics and Kafka integration.

## 🏗️ Project Structure

```
webshop-poc/
├── app/                    # FastAPI backend application
│   ├── routers/           # API route handlers
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── security.py        # Authentication & authorization
│   ├── kafka_config.py    # Kafka producer configuration
│   └── main.py           # Application entry point
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── context/       # React context providers
│   │   └── api/           # API client and types
│   └── package.json
├── scripts/               # Utility scripts
│   ├── migrations/        # Database migration scripts
│   ├── tests/            # Test scripts
│   ├── fixes/            # Database fix scripts
│   └── *.py              # General utility scripts
├── docs/                  # Documentation
├── tests/                 # Pytest test suite
├── uploads/               # File upload storage
├── docker-compose.kafka.yml # Kafka services configuration
└── webshop.db            # SQLite database
```

## 🚀 Quick Start

### Backend Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start Kafka services (optional but recommended):**
   ```bash
   docker-compose -f docker-compose.kafka.yml up -d
   ```

4. **Run the server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

## 📋 Features

- **Authentication & Authorization**: JWT-based auth with role-based access control
- **Product Management**: CRUD operations for products with image upload
- **Shopping Cart**: Add/remove items, quantity management
- **Order Management**: Create orders, view order history
- **Review System**: Product reviews with star ratings
- **Admin Panel**: Customer management, order overview
- **Image Upload**: Product image management with file storage
- **🆕 Kafka Integration**: Real-time analytics event streaming
- **🆕 Analytics Dashboard**: Comprehensive admin statistics panel with charts
- **🆕 Event Tracking**: Product, order, and user activity monitoring

## 🔥 New Features

### Kafka Integration
- **Real-time Event Streaming**: Track user actions, product views, and order activities
- **Analytics Events**: Product views, orders, user registrations, admin actions
- **Scalable Architecture**: Event-driven design for future analytics expansion

### Analytics Dashboard
- **📊 Overview**: Total revenue, orders, users, and products with trend charts
- **🛒 Orders Analytics**: Order statistics, today's metrics, top-selling products
- **👥 User Analytics**: User growth, active users, role-based counts
- **🛍️ Product Analytics**: Performance metrics, revenue per product, ratings
- **📈 Interactive Charts**: Revenue trends, order patterns, user growth visualization

## 🛠️ Scripts

### Database Management

- `scripts/populate_sample_data.py` - Populate database with sample data
- `scripts/check_schema.py` - Verify database schema
- `scripts/populate_usernames.py` - Add usernames to existing users

### Migrations

- `scripts/migrations/migrate_add_roles.py` - Add role-based user system
- `scripts/migrations/migrate_add_username.py` - Add username field
- `scripts/migrations/migrate_add_reviews.py` - Add review system
- `scripts/migrations/migrate_add_order_id.py` - Add order ID field
- `scripts/migrations/migrate_add_image_url.py` - Add image URL field

### Testing

- `scripts/tests/demo_auth_system.py` - Authentication system demo
- `scripts/tests/simple_test.py` - Basic API tests
- `scripts/tests/test_auth_roles.py` - Role-based access tests
- `scripts/tests/test_image_upload.py` - Image upload tests
- `scripts/tests/test_new_endpoints.py` - Endpoint functionality tests
- `scripts/tests/test_order_history_features.py` - Order history tests

## 📚 Documentation

- `docs/AUTHENTICATION_ROLES_SUMMARY.md` - Authentication and authorization guide
- `docs/IMAGE_UPLOAD_FEATURE.md` - Image upload functionality
- `docs/ORDER_HISTORY_AND_CUSTOMER_MANAGEMENT.md` - Order and customer management
- `docs/PRODUCT_IMAGES_SUMMARY.md` - Product image system overview
- `docs/REVIEW_SYSTEM.md` - Review and rating system
- `docs/KAFKA_INTEGRATION.md` - **🆕 Kafka integration and analytics guide**

## 🐳 Docker Support

### Kafka Services
```bash
# Start Kafka, Zookeeper, and Kafka UI
docker-compose -f docker-compose.kafka.yml up -d

# Access Kafka UI at http://localhost:8080
# Kafka broker available at localhost:9092
```

### Main Application
```bash
# Start the full application stack
docker-compose up -d
```

## 🔧 Configuration

### Environment Variables
```bash
# Kafka Configuration
KAFKA_ENABLED=true
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_ANALYTICS_TOPIC=webshop-analytics

# Admin Configuration
ADMIN_EMAIL=admin@webshop.com
ADMIN_PASSWORD=admin123

# Security
SECRET_KEY=your-secret-key-here
```

## 📊 Analytics API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/analytics/dashboard` | GET | Complete dashboard metrics | Admin |
| `/analytics/overview` | GET | System overview statistics | Admin |
| `/analytics/orders` | GET | Order analytics | Admin |
| `/analytics/users` | GET | User analytics | Admin |
| `/analytics/products` | GET | Product analytics | Admin |

## 🚀 Getting Started with Analytics

1. **Access the Dashboard**: Navigate to `/admin/statistics` as an admin user
2. **View Metrics**: Explore different tabs for comprehensive insights
3. **Monitor Events**: Check Kafka UI for real-time event streaming
4. **Customize**: Modify analytics calculations in `app/routers/analytics.py`

## 🔍 Monitoring & Debugging

- **Kafka UI**: http://localhost:8080 (when running Kafka services)
- **Backend Health**: `GET /health`
- **Analytics Health**: `GET /analytics/dashboard` (admin only)
- **Event Logs**: Check backend logs for Kafka events

## 🎯 Future Enhancements

- Real-time dashboard updates via WebSocket
- Advanced charting with Chart.js or D3.js
- Export analytics data to CSV/Excel
- Email reports and alerts
- Custom date range filtering
- Predictive analytics
- Redis caching for performance
- Multiple Kafka consumers for scalability
