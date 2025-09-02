import os
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from PIL import Image
from io import BytesIO
from ..database import get_db
from ..models import User
from ..deps import get_current_admin_user

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def is_valid_image_file(filename: str) -> bool:
    """Check if the file has a valid image extension"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def save_image(file: UploadFile) -> str:
    """Save uploaded image and return the filename"""
    try:
        # Read image data
        image_data = file.file.read()
        
        # Check file size
        if len(image_data) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large. Maximum size is 5MB."
            )
        
        # Validate image format
        try:
            image = Image.open(BytesIO(image_data))
            image.verify()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file."
            )
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save the image
        with open(file_path, "wb") as f:
            f.write(image_data)
        
        return unique_filename
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving image: {str(e)}"
        )


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_admin: User = Depends(get_current_admin_user)
):
    """Upload a product image"""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    if not is_valid_image_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    filename = save_image(file)
    
    return {
        "filename": filename,
        "url": f"/upload/uploads/{filename}"
    }


@router.get("/uploads/{filename}")
async def get_image(filename: str):
    """Serve uploaded images"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    return FileResponse(file_path)
