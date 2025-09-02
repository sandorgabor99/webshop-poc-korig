from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from ..database import get_db
from ..models import User, Product, Review
from ..schemas import ReviewCreate, ReviewUpdate, ReviewOut as ReviewSchema, ProductWithReviews
from ..deps import get_current_user

router = APIRouter()


@router.get("/product/{product_id}", response_model=List[ReviewSchema])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a specific product"""
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    return reviews


@router.get("/product/{product_id}/with-reviews", response_model=ProductWithReviews)
def get_product_with_reviews(product_id: int, db: Session = Depends(get_db)):
    """Get product with all its reviews"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    return product


@router.post("/", response_model=ReviewSchema)
def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new review for a product"""
    # Check if product exists
    product = db.query(Product).filter(Product.id == review_data.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    # Check if user already reviewed this product
    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.product_id == review_data.product_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You have already reviewed this product"
        )
    
    # Create new review
    db_review = Review(
        user_id=current_user.id,
        product_id=review_data.product_id,
        rating=review_data.rating,
        feedback=review_data.feedback
    )
    
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # Reload with user information
    db_review = db.query(Review).filter(Review.id == db_review.id).first()
    return db_review


@router.patch("/{review_id}", response_model=ReviewSchema)
def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing review"""
    # Find the review
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    # Check if user owns this review
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this review")
    
    # Update review
    update_data = review_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_review, field, value)
    
    db.commit()
    db.refresh(db_review)
    
    # Reload with user information
    db_review = db.query(Review).filter(Review.id == review_id).first()
    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a review"""
    # Find the review
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    # Check if user owns this review or is admin
    if db_review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this review")
    
    db.delete(db_review)
    db.commit()
    return None


@router.get("/user/me", response_model=List[ReviewSchema])
def get_user_reviews(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all reviews by the current user"""
    reviews = db.query(Review).filter(Review.user_id == current_user.id).all()
    return reviews
