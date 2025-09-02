# Product Review and Rating System

This document describes the comprehensive product review and rating system that has been implemented in the webshop application.

## Overview

The review system allows customers to rate products from 1-5 stars and provide optional feedback. The system includes:

- **Star Ratings**: 1-5 star rating system with visual star display
- **Customer Feedback**: Optional text feedback (up to 1000 characters)
- **Average Ratings**: Automatic calculation of product average ratings
- **Review Counts**: Display of total number of reviews per product
- **User Management**: Users can only review each product once
- **Review Management**: Users can edit/delete their own reviews, admins can delete any review

## Features

### For Customers
- **View Product Ratings**: See average star ratings and review counts on product cards
- **Read Reviews**: Browse all customer reviews with ratings and feedback
- **Write Reviews**: Submit star ratings and optional feedback for products
- **Manage Reviews**: Edit or delete their own reviews
- **One Review Per Product**: Users can only submit one review per product

### For Administrators
- **View All Reviews**: Access to all customer reviews across products
- **Delete Reviews**: Ability to remove inappropriate reviews
- **Review Analytics**: See average ratings and review counts for products

## Technical Implementation

### Backend Changes

#### 1. Database Schema
- **New Table**: `reviews` table with foreign keys to `users` and `products`
- **Product Model**: Added `average_rating` and `review_count` properties
- **User Model**: Added relationship to reviews

#### 2. New API Endpoints
- `GET /reviews/product/{product_id}` - Get all reviews for a product
- `GET /reviews/product/{product_id}/with-reviews` - Get product with all reviews
- `POST /reviews/` - Create a new review
- `PATCH /reviews/{review_id}` - Update an existing review
- `DELETE /reviews/{review_id}` - Delete a review
- `GET /reviews/user/me` - Get current user's reviews

#### 3. Updated Product Endpoints
- Product responses now include `average_rating` and `review_count` fields

### Frontend Changes

#### 1. New Components
- **StarRating**: Reusable star rating component with interactive and display modes
- **ReviewForm**: Form for submitting new reviews with rating and feedback
- **ReviewList**: Component to display list of reviews with user information

#### 2. New Pages
- **ProductDetail**: Detailed product page with reviews section
- **Enhanced Products**: Product cards now show ratings and review counts

#### 3. Updated API Client
- Added review-related API methods for all CRUD operations
- Updated product types to include rating information

## Database Schema

### Reviews Table
```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
```

### Indexes
- `idx_reviews_user_id` - For efficient user review queries
- `idx_reviews_product_id` - For efficient product review queries
- `idx_reviews_created_at` - For chronological sorting

## API Reference

### Review Schemas

#### ReviewCreate
```typescript
{
    product_id: number;
    rating: number; // 1-5
    feedback?: string; // Optional, max 1000 chars
}
```

#### Review
```typescript
{
    id: number;
    user_id: number;
    product_id: number;
    rating: number;
    feedback?: string;
    created_at: string;
    user: User;
}
```

#### Product (Updated)
```typescript
{
    // ... existing fields
    average_rating: number;
    review_count: number;
}
```

### Endpoints

#### Create Review
```http
POST /reviews/
Authorization: Bearer <token>
Content-Type: application/json

{
    "product_id": 1,
    "rating": 5,
    "feedback": "Great product!"
}
```

#### Get Product Reviews
```http
GET /reviews/product/1
```

#### Get Product with Reviews
```http
GET /reviews/product/1/with-reviews
```

#### Update Review
```http
PATCH /reviews/1
Authorization: Bearer <token>
Content-Type: application/json

{
    "rating": 4,
    "feedback": "Updated feedback"
}
```

#### Delete Review
```http
DELETE /reviews/1
Authorization: Bearer <token>
```

## User Interface

### Product Cards
- Display star rating with average score
- Show review count
- "Reviews" button to view detailed reviews

### Product Detail Page
- Large product image and details
- Prominent star rating display
- "Write a Review" button (if user hasn't reviewed)
- Complete list of customer reviews
- Review form for new submissions

### Review Components
- **Star Rating**: Interactive 5-star rating system
- **Review Form**: Rating selection and feedback textarea
- **Review List**: Individual review cards with user info and dates

## Security Features

1. **Authentication Required**: All review operations require user authentication
2. **One Review Per User**: Users can only submit one review per product
3. **Ownership Validation**: Users can only edit/delete their own reviews
4. **Admin Privileges**: Admins can delete any review
5. **Input Validation**: Rating must be 1-5, feedback limited to 1000 characters

## Migration

The system includes a migration script (`migrate_add_reviews.py`) that:
- Creates the reviews table with proper foreign keys
- Adds performance indexes
- Handles existing databases gracefully

## Usage Examples

### Creating a Review
```typescript
const review = await api.createReview({
    product_id: 1,
    rating: 5,
    feedback: "Excellent product quality!"
});
```

### Getting Product with Reviews
```typescript
const product = await api.getProductWithReviews(1);
console.log(`Average rating: ${product.average_rating}`);
console.log(`Review count: ${product.review_count}`);
```

### Displaying Star Rating
```tsx
<StarRating 
    rating={product.average_rating} 
    readonly 
    size="medium"
    showValue={true}
/>
```

## Future Enhancements

1. **Review Moderation**: Admin approval system for reviews
2. **Review Helpfulness**: Allow users to mark reviews as helpful
3. **Review Photos**: Allow customers to upload photos with reviews
4. **Review Analytics**: Detailed analytics for product performance
5. **Review Notifications**: Email notifications for new reviews
6. **Review Filtering**: Filter reviews by rating, date, helpfulness

## File Structure

```
app/
├── models.py              # Updated with Review model and Product properties
├── schemas.py             # Added review schemas
├── routers/
│   └── reviews.py         # New review endpoints
└── main.py               # Registered reviews router

frontend/
├── src/
│   ├── components/
│   │   ├── StarRating.tsx     # Star rating component
│   │   ├── ReviewForm.tsx     # Review submission form
│   │   └── ReviewList.tsx     # Review display component
│   ├── pages/
│   │   ├── Products.tsx       # Updated with ratings
│   │   └── ProductDetail.tsx  # New detailed product page
│   └── api/
│       ├── client.ts          # Added review API methods
│       └── types.ts           # Updated with review types

migrate_add_reviews.py    # Database migration script
```

## Testing

The review system includes comprehensive testing:
- API endpoint testing
- Component testing
- User interaction testing
- Error handling validation

## Performance Considerations

- Database indexes for efficient queries
- Lazy loading of reviews
- Caching of average ratings
- Optimized review counting

This review system provides a complete solution for customer feedback and product ratings, enhancing the shopping experience and providing valuable insights for both customers and administrators.
