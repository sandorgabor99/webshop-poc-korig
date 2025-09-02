from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta, timezone
from typing import List
import pandas as pd

from ..database import get_db
from ..deps import get_current_user, require_admin
from ..models import User, Product, Order, OrderItem, Review
from ..schemas import DashboardMetrics, SystemStatistics, OrderAnalytics, UserAnalytics, ProductAnalytics
from ..kafka_config import get_kafka_producer, KafkaProducer
from ..models import UserRole

router = APIRouter()

@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
    kafka: KafkaProducer = Depends(get_kafka_producer)
):
    """Get comprehensive dashboard metrics for admin panel"""
    try:
        # Send analytics event
        await kafka.send_user_event(
            "admin_dashboard_access",
            {"user_id": current_user.id, "role": current_user.role.value},
            current_user.id
        )
        
        # Calculate overview statistics
        overview = await get_system_statistics(db)
        
        # Calculate order analytics
        orders = await get_order_analytics(db)
        
        # Calculate user analytics
        users = await get_user_analytics(db)
        
        # Get product analytics
        products = await get_product_analytics(db)
        
        # Generate chart data
        revenue_chart = await get_revenue_chart_data(db)
        orders_chart = await get_orders_chart_data(db)
        
        # Calculate sales analytics
        sales_analytics = await get_sales_analytics(db)
        
        # Calculate rating analytics
        rating_analytics = await get_rating_analytics(db)
        
        return DashboardMetrics(
            overview=overview,
            orders=orders,
            users=users,
            products=products,
            revenue_chart=revenue_chart,
            orders_chart=orders_chart,
            sales_analytics=sales_analytics,
            rating_analytics=rating_analytics
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard metrics: {str(e)}")

@router.get("/overview", response_model=SystemStatistics)
async def get_system_overview(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get system overview statistics"""
    return await get_system_statistics(db)

@router.get("/orders", response_model=OrderAnalytics)
async def get_order_analytics_endpoint(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get order analytics"""
    return await get_order_analytics(db)

@router.get("/users", response_model=UserAnalytics)
async def get_user_analytics_endpoint(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get user analytics"""
    return await get_user_analytics(db)

@router.get("/products", response_model=List[ProductAnalytics])
async def get_product_analytics_endpoint(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get product analytics"""
    return await get_product_analytics(db)

# Helper functions
async def get_system_statistics(db: Session) -> SystemStatistics:
    """Calculate system overview statistics"""
    # Total counts
    total_products = db.query(Product).count()
    total_orders = db.query(Order).count()
    total_users = db.query(User).count()
    
    # Total revenue
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0.0
    
    # Average product rating
    avg_rating = db.query(func.avg(Review.rating)).scalar() or 0.0
    
    # Top selling products
    top_products = await get_top_selling_products(db, limit=5)
    
    # Recent orders
    recent_orders = db.query(Order).order_by(desc(Order.created_at)).limit(10).all()
    recent_orders_data = [
        {
            "id": order.id,
            "order_id": order.order_id,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "user_email": order.user.email if order.user else "Unknown"
        }
        for order in recent_orders
    ]
    
    # User growth (last 7 days)
    user_growth = await get_user_growth_data(db)
    
    # Basic sales metrics
    sales_metrics = {
        "total_revenue": float(total_revenue),
        "total_orders": total_orders,
        "average_order_value": round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0
    }
    
    # Basic rating metrics
    total_reviews = db.query(Review).count()
    positive_reviews = db.query(Review).filter(Review.rating >= 4).count()
    rating_metrics = {
        "total_reviews": total_reviews,
        "average_rating": round(float(avg_rating), 2),
        "positive_percentage": round((positive_reviews / total_reviews * 100), 2) if total_reviews > 0 else 0.0
    }
    
    return SystemStatistics(
        total_products=total_products,
        total_orders=total_orders,
        total_users=total_users,
        total_revenue=total_revenue,
        average_product_rating=round(avg_rating, 1),
        top_selling_products=top_products,
        recent_orders=recent_orders_data,
        user_growth=user_growth,
        sales_metrics=sales_metrics,
        rating_metrics=rating_metrics
    )

async def get_order_analytics(db: Session) -> OrderAnalytics:
    """Calculate order analytics"""
    today = datetime.now(timezone.utc).date()
    
    # Total orders and revenue
    total_orders = db.query(Order).count()
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0.0
    
    # Today's orders and revenue
    orders_today = db.query(Order).filter(
        func.date(Order.created_at) == today
    ).count()
    
    revenue_today = db.query(func.sum(Order.total_amount)).filter(
        func.date(Order.created_at) == today
    ).scalar() or 0.0
    
    # Average order value
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    
    # Top products
    top_products = await get_top_selling_products(db, limit=5)
    
    # Sales by category (simplified - all products in one category for now)
    sales_by_category = [
        {
            "category": "All Products",
            "orders": total_orders,
            "revenue": float(total_revenue)
        }
    ]
    
    # Monthly sales (last 6 months)
    six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)
    monthly_sales = db.query(
        func.strftime('%Y-%m', Order.created_at).label('month'),
        func.count(Order.id).label('order_count'),
        func.sum(Order.total_amount).label('total_revenue')
    ).filter(Order.created_at >= six_months_ago)\
     .group_by(func.strftime('%Y-%m', Order.created_at))\
     .order_by(func.strftime('%Y-%m', Order.created_at))\
     .all()
    
    monthly_sales_data = [
        {
            "month": month.month,
            "orders": int(month.order_count or 0),
            "revenue": float(month.total_revenue or 0)
        }
        for month in monthly_sales
    ]
    
    return OrderAnalytics(
        total_orders=total_orders,
        total_revenue=total_revenue,
        average_order_value=round(average_order_value, 2),
        orders_today=orders_today,
        revenue_today=revenue_today,
        top_products=top_products,
        sales_by_category=sales_by_category,
        monthly_sales=monthly_sales_data
    )

async def get_user_analytics(db: Session) -> UserAnalytics:
    """Calculate user analytics"""
    today = datetime.now(timezone.utc).date()
    
    # Total users
    total_users = db.query(User).count()
    
    # New users today
    new_users_today = db.query(User).filter(
        func.date(User.created_at) == today
    ).count()
    
    # Active users (users with orders in last 30 days)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    active_users = db.query(User).join(Order).filter(
        Order.created_at >= thirty_days_ago
    ).distinct().count()
    
    # User counts by role
    admin_users = db.query(User).filter(User.role == UserRole.ADMINISTRATOR).count()
    customer_users = db.query(User).filter(User.role == UserRole.CUSTOMER).count()
    
    # Calculate user engagement (percentage of users who have placed orders)
    total_users_with_orders = db.query(User).join(Order).distinct().count()
    user_engagement = (total_users_with_orders / total_users * 100) if total_users > 0 else 0.0
    
    return UserAnalytics(
        total_users=total_users,
        new_users_today=new_users_today,
        active_users=active_users,
        admin_users=admin_users,
        customer_users=customer_users,
        user_engagement=round(user_engagement, 2)
    )

async def get_product_analytics(db: Session) -> List[ProductAnalytics]:
    """Calculate product analytics"""
    products = db.query(Product).all()
    analytics = []
    
    for product in products:
        # Count orders for this product
        orders_count = db.query(OrderItem).filter(
            OrderItem.product_id == product.id
        ).count()
        
        # Calculate revenue for this product
        revenue = db.query(func.sum(OrderItem.unit_price * OrderItem.quantity)).filter(
            OrderItem.product_id == product.id
        ).scalar() or 0.0
        
        analytics.append(ProductAnalytics(
            product_id=product.id,
            product_name=product.name,
            views=0,  # Would need to implement view tracking
            orders=orders_count,
            revenue=revenue,
            average_rating=product.average_rating,
            review_count=product.review_count,
            stock_level=product.stock,
            profit_margin=0.0  # Would need cost data to calculate actual profit margin
        ))
    
    # Sort by revenue
    analytics.sort(key=lambda x: x.revenue, reverse=True)
    return analytics

async def get_top_selling_products(db: Session, limit: int = 5) -> List[ProductAnalytics]:
    """Get top selling products by order count"""
    # Get products with their order counts
    product_stats = db.query(
        Product.id,
        Product.name,
        func.count(OrderItem.id).label('order_count'),
        func.sum(OrderItem.unit_price * OrderItem.quantity).label('revenue')
    ).join(OrderItem, Product.id == OrderItem.product_id, isouter=True)\
     .group_by(Product.id, Product.name)\
     .order_by(desc('order_count'))\
     .limit(limit)\
     .all()
    
    return [
        ProductAnalytics(
            product_id=stat.id,
            product_name=stat.name,
            orders=stat.order_count or 0,
            revenue=stat.revenue or 0.0,
            average_rating=0.0,  # Would need to join with reviews
            review_count=0
        )
        for stat in product_stats
    ]

async def get_revenue_chart_data(db: Session) -> List[dict]:
    """Get revenue data for charts (last 30 days)"""
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    
    # Get daily revenue
    daily_revenue = db.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(Order.created_at >= thirty_days_ago)\
     .group_by(func.date(Order.created_at))\
     .order_by(func.date(Order.created_at))\
     .all()
    
    return [
        {"date": str(day.date), "revenue": float(day.revenue or 0)}
        for day in daily_revenue
    ]

async def get_orders_chart_data(db: Session) -> List[dict]:
    """Get orders data for charts (last 30 days)"""
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    
    # Get daily orders
    daily_orders = db.query(
        func.date(Order.created_at).label('date'),
        func.count(Order.id).label('order_count')
    ).filter(Order.created_at >= thirty_days_ago)\
     .group_by(func.date(Order.created_at))\
     .order_by(func.date(Order.created_at))\
     .all()
    
    return [
        {"date": str(day.date), "orders": int(day.order_count or 0)}
        for day in daily_orders
    ]

async def get_user_growth_data(db: Session) -> dict:
    """Get user growth data for charts (last 7 days)"""
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    
    # Get daily new users
    daily_users = db.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('user_count')
    ).filter(User.created_at >= seven_days_ago)\
     .group_by(func.date(User.created_at))\
     .order_by(func.date(User.created_at))\
     .all()
    
    return {
        "labels": [str(day.date) for day in daily_users],
        "data": [int(day.user_count or 0) for day in daily_users]
    }

async def get_sales_analytics(db: Session) -> dict:
    """Calculate comprehensive sales analytics"""
    try:
        print("Starting sales analytics calculation...")
        
        # Monthly sales for the last 12 months
        twelve_months_ago = datetime.now(timezone.utc) - timedelta(days=365)
        print(f"Querying orders from: {twelve_months_ago}")
        
        # Use date() function for SQLite compatibility
        monthly_sales = db.query(
            func.strftime('%Y-%m', Order.created_at).label('month'),
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('total_revenue')
        ).filter(Order.created_at >= twelve_months_ago)\
         .group_by(func.strftime('%Y-%m', Order.created_at))\
         .order_by(func.strftime('%Y-%m', Order.created_at))\
         .all()
        
        print(f"Monthly sales query result: {monthly_sales}")
        
        # Sales by day of week (0=Sunday, 1=Monday, etc.)
        day_of_week_sales = db.query(
            func.strftime('%w', Order.created_at).label('day_of_week'),
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('total_revenue')
        ).group_by(func.strftime('%w', Order.created_at))\
         .order_by(func.strftime('%w', Order.created_at))\
         .all()
        
        print(f"Day of week sales query result: {day_of_week_sales}")
        
        # Top performing time slots (hourly)
        hourly_sales = db.query(
            func.strftime('%H', Order.created_at).label('hour'),
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('total_revenue')
        ).group_by(func.strftime('%H', Order.created_at))\
         .order_by(func.strftime('%H', Order.created_at))\
         .all()
        
        print(f"Hourly sales query result: {hourly_sales}")
        
        # Calculate conversion rate (orders per user)
        total_users = db.query(User).count()
        total_orders = db.query(Order).count()
        conversion_rate = (total_orders / total_users * 100) if total_users > 0 else 0
        
        print(f"Total users: {total_users}, Total orders: {total_orders}, Conversion rate: {conversion_rate}%")
        
        # Generate month range for the last 12 months
        month_range = []
        for i in range(12):
            month_date = datetime.now(timezone.utc) - timedelta(days=30*i)
            month_str = month_date.strftime('%Y-%m')
            month_range.append(month_str)
        
        # Process monthly sales data
        monthly_sales_data = []
        for month in month_range:
            month_data = next((item for item in monthly_sales if item[0] == month), None)
            if month_data:
                monthly_sales_data.append({
                    'month': month,
                    'orders': month_data[1],
                    'revenue': float(month_data[2])
                })
            else:
                monthly_sales_data.append({
                    'month': month,
                    'orders': 0,
                    'revenue': 0.0
                })
        
        # Reverse the order so latest month comes first
        monthly_sales_data.reverse()
        
        print(f"Processed monthly sales data: {monthly_sales_data}")
        
        # Ensure we have data for all days of week
        day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day_of_week_data = []
        for day_num in range(7):
            existing_day = next((d for d in day_of_week_sales if d.day_of_week == day_num), None)
            if existing_day:
                day_of_week_data.append({
                    "day": int(existing_day.day_of_week),
                    "day_name": day_names[day_num],
                    "orders": int(existing_day.order_count or 0),
                    "revenue": float(existing_day.total_revenue or 0)
                })
            else:
                day_of_week_data.append({
                    "day": day_num,
                    "day_name": day_names[day_num],
                    "orders": 0,
                    "revenue": 0.0
                })
        
        # Ensure we have data for all hours
        hourly_data = []
        for hour in range(24):
            existing_hour = next((h for h in hourly_sales if h.hour == hour), None)
            if existing_hour:
                hourly_data.append({
                    "hour": int(existing_hour.hour),
                    "orders": int(existing_hour.order_count or 0),
                    "revenue": float(existing_hour.total_revenue or 0)
                })
            else:
                hourly_data.append({
                    "hour": hour,
                    "orders": 0,
                    "revenue": 0.0
                })
        
        result = {
            "monthly_sales": monthly_sales_data,
            "day_of_week_sales": day_of_week_data,
            "hourly_sales": hourly_data,
            "conversion_rate": round(conversion_rate, 2),
            "total_customers": total_users,
            "total_orders": total_orders
        }
        
        print(f"Sales analytics result: {result}")
        return result
        
    except Exception as e:
        print(f"Error in sales analytics: {e}")
        import traceback
        traceback.print_exc()
        return {
            "monthly_sales": [],
            "day_of_week_sales": [],
            "hourly_sales": [],
            "conversion_rate": 0.0,
            "total_customers": 0,
            "total_orders": 0
        }

async def get_rating_analytics(db: Session) -> dict:
    """Calculate comprehensive rating analytics"""
    try:
        print("Starting rating analytics calculation...")
        
        # Overall rating distribution
        rating_distribution = db.query(
            Review.rating,
            func.count(Review.id).label('count')
        ).group_by(Review.rating)\
         .order_by(Review.rating)\
         .all()
        
        print(f"Rating distribution query result: {rating_distribution}")
        
        # Average rating by product category (if categories exist)
        product_ratings = db.query(
            Product.id,
            Product.name,
            func.avg(Review.rating).label('average_rating'),
            func.count(Review.id).label('review_count')
        ).join(Review, Product.id == Review.product_id, isouter=True)\
         .group_by(Product.id, Product.name)\
         .having(func.count(Review.id) > 0)\
         .order_by(desc(func.avg(Review.rating)))\
         .limit(10)\
         .all()
        
        print(f"Product ratings query result: {product_ratings}")
        
        # Rating trends over time (last 30 days)
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        rating_trends = db.query(
            func.date(Review.created_at).label('date'),
            func.avg(Review.rating).label('avg_rating'),
            func.count(Review.id).label('review_count')
        ).filter(Review.created_at >= thirty_days_ago)\
         .group_by(func.date(Review.created_at))\
         .order_by(func.date(Review.created_at))\
         .all()
        
        print(f"Rating trends query result: {rating_trends}")
        
        # Calculate overall statistics
        total_reviews = db.query(Review).count()
        avg_rating = db.query(func.avg(Review.rating)).scalar() or 0.0
        products_with_reviews = db.query(Product).join(Review, Product.id == Review.product_id).distinct().count()
        
        print(f"Total reviews: {total_reviews}, Avg rating: {avg_rating}, Products with reviews: {products_with_reviews}")
        
        # Rating sentiment analysis
        positive_reviews = db.query(Review).filter(Review.rating >= 4).count()
        neutral_reviews = db.query(Review).filter(Review.rating == 3).count()
        negative_reviews = db.query(Review).filter(Review.rating <= 2).count()
        
        print(f"Positive: {positive_reviews}, Neutral: {neutral_reviews}, Negative: {negative_reviews}")
        
        result = {
            "rating_distribution": [
                {
                    "rating": int(rating.rating),
                    "count": int(rating.count),
                    "percentage": round((int(rating.count) / total_reviews * 100), 2) if total_reviews > 0 else 0
                }
                for rating in rating_distribution
            ],
            "top_rated_products": [
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "average_rating": float(product.average_rating or 0),
                    "review_count": int(product.review_count or 0)
                }
                for product in product_ratings
            ],
            "rating_trends": [
                {
                    "date": str(trend.date),
                    "average_rating": float(trend.avg_rating or 0),
                    "review_count": int(trend.review_count or 0)
                }
                for trend in rating_trends
            ],
            "overall_stats": {
                "total_reviews": total_reviews,
                "average_rating": round(float(avg_rating), 2),
                "products_with_reviews": products_with_reviews,
                "positive_reviews": positive_reviews,
                "neutral_reviews": neutral_reviews,
                "negative_reviews": negative_reviews,
                "positive_percentage": round((positive_reviews / total_reviews * 100), 2) if total_reviews > 0 else 0
            }
        }
        
        print(f"Rating analytics result: {result}")
        return result
        
    except Exception as e:
        print(f"Error in rating analytics: {e}")
        import traceback
        traceback.print_exc()
        return {
            "rating_distribution": [],
            "top_rated_products": [],
            "rating_trends": [],
            "overall_stats": {
                "total_reviews": 0,
                "average_rating": 0.0,
                "products_with_reviews": 0,
                "positive_reviews": 0,
                "neutral_reviews": 0,
                "negative_reviews": 0,
                "positive_percentage": 0.0
            }
        }
