from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from ..models import User, Product, Order, OrderItem, UserRole
from ..schemas import OrderItemIn, OrderOut, OrderWithDetails, CustomerOrderSummary
from ..deps import get_current_user, require_admin

router = APIRouter()


@router.post("/", response_model=OrderOut)
def create_order(
    order_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items = order_data.get("items", [])
    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No items in order"
        )
    
    total_amount = 0
    order_items = []
    
    for item_data in items:
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item_data['product_id']} not found"
            )
        
        if product.stock < item_data["quantity"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )
        
        # Update stock
        product.stock -= item_data["quantity"]
        
        # Calculate total
        item_total = product.price * item_data["quantity"]
        total_amount += item_total
        
        # Create order item
        order_item = OrderItem(
            product_id=product.id,
            quantity=item_data["quantity"],
            unit_price=product.price
        )
        order_items.append(order_item)
    
    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Add order items
    for item in order_items:
        item.order_id = order.id
        db.add(item)
    
    db.commit()
    db.refresh(order)
    
    return order


@router.get("/", response_model=List[OrderOut])
def list_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@router.get("/detailed", response_model=List[OrderWithDetails])
def list_my_orders_detailed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed order history for the current user with product information"""
    from sqlalchemy.orm import joinedload
    
    orders = db.query(Order)\
        .options(joinedload(Order.items).joinedload(OrderItem.product))\
        .filter(Order.user_id == current_user.id)\
        .order_by(Order.created_at.desc())\
        .all()
    return orders


@router.get("/summary", response_model=CustomerOrderSummary)
def get_my_order_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get order summary statistics for the current user"""
    # Get order statistics
    result = db.query(
        func.count(Order.id).label('total_orders'),
        func.coalesce(func.sum(Order.total_amount), 0).label('total_spent'),
        func.coalesce(func.avg(Order.total_amount), 0).label('average_order_value'),
        func.max(Order.created_at).label('last_order_date')
    ).filter(Order.user_id == current_user.id).first()
    
    return CustomerOrderSummary(
        total_orders=result.total_orders or 0,
        total_spent=float(result.total_spent or 0),
        average_order_value=float(result.average_order_value or 0),
        last_order_date=result.last_order_date
    )


@router.get("/{order_id}", response_model=OrderWithDetails)
def get_order_details(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific order"""
    from sqlalchemy.orm import joinedload
    
    order = db.query(Order)\
        .options(joinedload(Order.items).joinedload(OrderItem.product))\
        .filter(Order.id == order_id)\
        .first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user can access this order
    if order.user_id != current_user.id and current_user.role != UserRole.ADMINISTRATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return order


# Admin endpoints
@router.get("/admin/all", response_model=List[OrderWithDetails])
def list_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, description="Search by order ID"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to list all orders with pagination and search"""
    from sqlalchemy.orm import joinedload
    
    query = db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product))
    
    # Add search filter if provided
    if search:
        query = query.filter(Order.order_id.ilike(f"%{search}%"))
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders


@router.get("/admin/search/{order_id}", response_model=OrderWithDetails)
def search_order_by_id(
    order_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to search for a specific order by order_id"""
    from sqlalchemy.orm import joinedload
    
    order = db.query(Order)\
        .options(joinedload(Order.items).joinedload(OrderItem.product))\
        .filter(Order.order_id == order_id)\
        .first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.get("/admin/customer/{user_id}", response_model=List[OrderWithDetails])
def list_customer_orders(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to list all orders for a specific customer"""
    from sqlalchemy.orm import joinedload
    
    # Verify customer exists
    customer = db.query(User).filter(User.id == user_id, User.role == UserRole.CUSTOMER).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    orders = db.query(Order)\
        .options(joinedload(Order.items).joinedload(OrderItem.product))\
        .filter(Order.user_id == user_id)\
        .order_by(Order.created_at.desc())\
        .all()
    return orders
