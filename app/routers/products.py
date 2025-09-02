from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from ..database import get_db
from ..models import User, Product, OrderItem
from ..schemas import ProductCreate, ProductUpdate, Product as ProductSchema
from ..deps import get_current_user, get_current_admin_user
from ..kafka_config import get_kafka_producer, KafkaProducer

router = APIRouter()


@router.get("/", response_model=List[ProductSchema])
async def list_products(
    db: Session = Depends(get_db),
    kafka: KafkaProducer = Depends(get_kafka_producer)
):
    products = db.query(Product).all()
    
    # Send analytics event for product listing
    try:
        await kafka.send_analytics_event(
            "product_list_viewed",
            {"product_count": len(products), "timestamp": "now"}
        )
    except Exception as e:
        # Log error but don't fail the request
        pass
    
    return products


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: int, 
    db: Session = Depends(get_db),
    kafka: KafkaProducer = Depends(get_kafka_producer)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    # Send analytics event for product view
    try:
        await kafka.send_product_event(
            "product_viewed",
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "created_at": product.created_at.isoformat() if product.created_at else None
            }
        )
    except Exception as e:
        # Log error but don't fail the request
        pass
    
    return product


@router.post("/", response_model=ProductSchema)
async def create_product(
    product_data: ProductCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    kafka: KafkaProducer = Depends(get_kafka_producer)
):
    db_product = Product(**product_data.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Send analytics event for product creation
    try:
        await kafka.send_product_event(
            "product_created",
            {
                "id": db_product.id,
                "name": db_product.name,
                "price": db_product.price,
                "created_at": db_product.created_at.isoformat() if db_product.created_at else None
            },
            current_admin.id
        )
    except Exception as e:
        # Log error but don't fail the request
        pass
    
    return db_product


@router.patch("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    kafka: KafkaProducer = Depends(get_kafka_producer)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    
    # Send analytics event for product update
    try:
        await kafka.send_product_event(
            "product_updated",
            {
                "id": db_product.id,
                "name": db_product.name,
                "price": db_product.price,
                "updated_fields": list(update_data.keys()),
                "created_at": db_product.created_at.isoformat() if db_product.created_at else None
            },
            current_admin.id
        )
    except Exception as e:
        # Log error but don't fail the request
        pass
    
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    kafka: KafkaProducer = Depends(get_kafka_producer)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    # Store product info for analytics before deletion
    product_info = {
        "id": db_product.id,
        "name": db_product.name,
        "price": db_product.price,
        "created_at": db_product.created_at.isoformat() if db_product.created_at else None
    }
    
    try:
        # Check if product has order items
        order_items = db.query(OrderItem).filter(OrderItem.product_id == product_id).count()
        if order_items > 0:
            # Delete all order items first
            db.query(OrderItem).filter(OrderItem.product_id == product_id).delete()
        
        # Now delete the product
        db.delete(db_product)
        db.commit()
        
        # Send analytics event for product deletion
        try:
            await kafka.send_product_event(
                "product_deleted",
                {**product_info, "order_items_deleted": order_items},
                current_admin.id
            )
        except Exception as e:
            # Log error but don't fail the request
            pass
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete product: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )
    
    return None
