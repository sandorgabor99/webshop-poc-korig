# Kafka Integration & Analytics Dashboard

This document describes the Kafka integration and analytics dashboard features added to the WebShop POC.

## Overview

The WebShop POC now includes:
- **Kafka Integration**: Real-time analytics event streaming
- **Analytics Dashboard**: Comprehensive admin statistics panel
- **Event Tracking**: Product, order, and user activity monitoring

## Architecture

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

## Features

### 1. Kafka Integration

#### Event Types
- **Product Events**: `product_viewed`, `product_created`, `product_updated`, `product_deleted`
- **Order Events**: `order_created`, `order_completed`
- **User Events**: `user_registered`, `user_login`, `admin_dashboard_access`
- **Analytics Events**: `product_list_viewed`, `cart_updated`

#### Event Schema
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

### 2. Analytics Dashboard

#### Overview Tab
- Total revenue, orders, users, and products
- Revenue trend chart (last 30 days)
- Orders trend chart (last 30 days)
- Recent orders table

#### Orders Tab
- Order statistics and metrics
- Today's orders and revenue
- Top selling products
- Average order value

#### Users Tab
- User growth analytics
- Active user metrics
- Role-based user counts
- User growth chart (last 7 days)

#### Products Tab
- Product performance metrics
- Order counts and revenue per product
- Rating and review analytics
- Performance comparison

## Setup Instructions

### 1. Install Dependencies

```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
```

### 2. Start Kafka Services

```bash
# Start Kafka, Zookeeper, and Kafka UI
docker-compose -f docker-compose.kafka.yml up -d

# Verify services are running
docker-compose -f docker-compose.kafka.yml ps
```

### 3. Configure Environment

```bash
# Copy environment file
cp env.example .env

# Edit .env file with your settings
KAFKA_ENABLED=true
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_ANALYTICS_TOPIC=webshop-analytics
```

### 4. Start the Application

```bash
# Start backend
uvicorn app.main:app --reload

# Start frontend (in another terminal)
cd frontend
npm run dev
```

## API Endpoints

### Analytics Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/analytics/dashboard` | GET | Complete dashboard metrics | Admin |
| `/analytics/overview` | GET | System overview statistics | Admin |
| `/analytics/orders` | GET | Order analytics | Admin |
| `/analytics/users` | GET | User analytics | Admin |
| `/analytics/products` | GET | Product analytics | Admin |

### Kafka Topics

- **`webshop-analytics`**: Main analytics events topic
- **`webshop-products`**: Product-related events
- **`webshop-orders`**: Order-related events
- **`webshop-users`**: User-related events

## Event Tracking

### Product Events
```python
# Product viewed
await kafka.send_product_event("product_viewed", product_data)

# Product created
await kafka.send_product_event("product_created", product_data, admin_user_id)

# Product updated
await kafka.send_product_event("product_updated", product_data, admin_user_id)
```

### Order Events
```python
# Order created
await kafka.send_order_event("order_created", order_data, user_id)

# Order completed
await kafka.send_order_event("order_completed", order_data, user_id)
```

### User Events
```python
# User registered
await kafka.send_user_event("user_registered", user_data, user_id)

# Admin dashboard access
await kafka.send_user_event("admin_dashboard_access", user_data, user_id)
```

## Monitoring & Debugging

### Kafka UI
Access the Kafka UI at `http://localhost:8080` to:
- View topics and messages
- Monitor consumer groups
- Inspect message content
- Manage topics

### Logs
```bash
# Backend logs
tail -f logs/app.log

# Kafka logs
docker-compose -f docker-compose.kafka.yml logs -f kafka
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Kafka connectivity
curl http://localhost:8000/analytics/dashboard
```

## Performance Considerations

### Event Batching
- Events are sent asynchronously
- Non-blocking event transmission
- Graceful fallback if Kafka is unavailable

### Database Optimization
- Analytics queries use database indexes
- Cached calculations for frequently accessed metrics
- Efficient aggregation queries

### Frontend Performance
- Lazy loading of chart data
- Responsive design for mobile devices
- Optimized re-renders with React hooks

## Security

### Access Control
- All analytics endpoints require admin authentication
- JWT token validation
- Role-based access control

### Data Privacy
- User IDs are anonymized in analytics events
- Sensitive data is not logged
- GDPR-compliant data handling

## Troubleshooting

### Common Issues

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

### Debug Mode
```python
# Enable debug logging in config.py
KAFKA_DEBUG = True
```

## Future Enhancements

### Planned Features
- Real-time dashboard updates via WebSocket
- Advanced charting with Chart.js or D3.js
- Export analytics data to CSV/Excel
- Email reports and alerts
- Custom date range filtering
- Predictive analytics

### Scalability Improvements
- Redis caching for analytics data
- Event streaming with multiple consumers
- Horizontal scaling of Kafka cluster
- Data retention policies
- Backup and recovery procedures

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify Kafka services are running
3. Review environment configuration
4. Check network connectivity
5. Consult the troubleshooting section

## Contributing

To add new analytics events:
1. Define event schema in `schemas.py`
2. Add event sending in relevant router
3. Update analytics calculations
4. Add frontend visualization
5. Update documentation
