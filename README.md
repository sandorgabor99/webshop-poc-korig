# WebShop POC

A full-stack e-commerce proof of concept with FastAPI backend and React frontend.

## 🏗️ Project Structure

```
webshop-poc/
├── app/                    # FastAPI backend application
│   ├── routers/           # API route handlers
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── security.py        # Authentication & authorization
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

3. **Run the server:**
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

### Database Fixes

- `scripts/fixes/fix_admin_username.py` - Fix admin username issues
- `scripts/fixes/fix_database.py` - General database fixes
- `scripts/fixes/fix_product_images.py` - Fix product image URLs
- `scripts/fixes/improve_product_images.py` - Enhance product images
- `scripts/fixes/quick_fix.py` - Quick database fixes

## 📚 Documentation

- `docs/AUTHENTICATION_ROLES_SUMMARY.md` - Authentication system overview
- `docs/IMAGE_UPLOAD_FEATURE.md` - Image upload functionality
- `docs/ORDER_HISTORY_AND_CUSTOMER_MANAGEMENT.md` - Order and customer management
- `docs/PRODUCT_IMAGES_SUMMARY.md` - Product image system
- `docs/REVIEW_SYSTEM.md` - Review and rating system

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 🔧 Development

### Database

The application uses SQLite for simplicity. The database file is `webshop.db`.

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Environment Variables

Copy `env.example` to `.env` and configure:
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## 📝 License

This is a proof of concept project for educational purposes.
