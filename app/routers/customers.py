from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from ..models import User, Order, UserRole
from ..schemas import UserOut, UserWithOrders, CustomerOrderSummary
from ..deps import require_admin

router = APIRouter()


@router.get("/", response_model=List[UserWithOrders])
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to list all customers with their order statistics"""
    # Get customers with their order statistics
    customers = db.query(
        User.id,
        User.email,
        User.username,
        User.role,
        User.created_at,
        func.count(Order.id).label('order_count'),
        func.coalesce(func.sum(Order.total_amount), 0).label('total_spent')
    ).outerjoin(Order, User.id == Order.user_id)\
     .filter(User.role == UserRole.CUSTOMER)\
     .group_by(User.id)\
     .order_by(User.created_at.desc())\
     .offset(skip)\
     .limit(limit)\
     .all()
    
    result = []
    for customer in customers:
        # Handle cases where username might be null for existing users
        username = customer.username or f"user_{customer.id}"
        
        result.append(UserWithOrders(
            id=customer.id,
            email=customer.email,
            username=username,
            role=customer.role,
            is_admin=customer.role == UserRole.ADMINISTRATOR,
            created_at=customer.created_at,
            order_count=customer.order_count or 0,
            total_spent=float(customer.total_spent or 0)
        ))
    
    return result


@router.get("/{user_id}", response_model=UserOut)
def get_customer(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to get detailed information about a specific customer"""
    customer = db.query(User).filter(User.id == user_id, User.role == UserRole.CUSTOMER).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer


@router.get("/{user_id}/orders", response_model=List[UserOut])
def get_customer_order_history(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to get order history for a specific customer"""
    # This endpoint is redundant with /orders/admin/customer/{user_id}
    # but kept for consistency in customer management
    customer = db.query(User).filter(User.id == user_id, User.role == UserRole.CUSTOMER).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return [customer]


@router.get("/{user_id}/summary", response_model=CustomerOrderSummary)
def get_customer_order_summary(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to get order summary statistics for a specific customer"""
    # Verify customer exists
    customer = db.query(User).filter(User.id == user_id, User.role == UserRole.CUSTOMER).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Get order statistics
    result = db.query(
        func.count(Order.id).label('total_orders'),
        func.coalesce(func.sum(Order.total_amount), 0).label('total_spent'),
        func.coalesce(func.avg(Order.total_amount), 0).label('average_order_value'),
        func.max(Order.created_at).label('last_order_date')
    ).filter(Order.user_id == user_id).first()
    
    return CustomerOrderSummary(
        total_orders=result.total_orders or 0,
        total_spent=float(result.total_spent or 0),
        average_order_value=float(result.average_order_value or 0),
        last_order_date=result.last_order_date
    )
