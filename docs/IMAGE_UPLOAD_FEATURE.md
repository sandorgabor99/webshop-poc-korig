# Product Image Upload Feature

This document describes the new product image upload functionality that has been added to the webshop application.

## Overview

The image upload feature allows administrators to upload and manage product images through the admin interface. Images are stored locally on the server and served through a dedicated endpoint.

## Features

### Backend Features
- **Image Upload Endpoint**: `/upload/image` - Secure endpoint for uploading product images
- **Image Serving**: `/upload/uploads/{filename}` - Serves uploaded images
- **File Validation**: Validates file type, size, and image format
- **Security**: Admin-only access to upload functionality
- **Database Integration**: Product model updated with `image_url` field

### Frontend Features
- **Image Upload Component**: Reusable `ImageUpload` component with drag-and-drop functionality
- **Admin Interface**: Updated product management page with image upload
- **Product Display**: Products page now displays product images
- **Preview Functionality**: Real-time image preview during upload
- **Error Handling**: Comprehensive error messages for upload failures

## Technical Implementation

### Backend Changes

#### 1. Database Schema
- Added `image_url` column to the `products` table
- Migration script provided for existing databases

#### 2. New Dependencies
- `Pillow==10.4.0` - For image processing and validation
- `python-multipart` - Already included for file uploads

#### 3. New Files
- `app/routers/upload.py` - Image upload router
- `migrate_add_image_url.py` - Database migration script

#### 4. Updated Files
- `app/models.py` - Added image_url field to Product model
- `app/schemas.py` - Updated product schemas to include image_url
- `app/main.py` - Registered upload router

### Frontend Changes

#### 1. New Components
- `frontend/src/components/ImageUpload.tsx` - Reusable image upload component

#### 2. Updated Files
- `frontend/src/api/client.ts` - Added uploadImage method
- `frontend/src/api/types.ts` - Updated Product types to include image_url
- `frontend/src/pages/AdminProducts.tsx` - Added image upload to admin interface
- `frontend/src/pages/Products.tsx` - Added image display to product cards

## Usage

### For Administrators

1. **Uploading Product Images**:
   - Navigate to the Admin Products page
   - In the "Create New Product" form, click the image upload area
   - Select an image file (JPG, PNG, GIF, WebP, max 5MB)
   - The image will be uploaded and previewed
   - Create the product with the uploaded image

2. **Managing Existing Product Images**:
   - View product images in the products table
   - Use the "Edit Image" button (feature coming soon)

### For Users

- Product images are automatically displayed on the Products page
- Images are shown in product cards with fallback to placeholder
- Images are responsive and maintain aspect ratio

## File Structure

```
uploads/                    # Uploaded images directory
├── {uuid}.jpg            # Individual image files
├── {uuid}.png
└── ...

app/
├── routers/
│   └── upload.py         # Image upload endpoints
├── models.py             # Updated Product model
├── schemas.py            # Updated product schemas
└── main.py               # Registered upload router

frontend/
├── src/
│   ├── components/
│   │   └── ImageUpload.tsx    # Image upload component
│   ├── api/
│   │   ├── client.ts          # Added uploadImage method
│   │   └── types.ts           # Updated Product types
│   └── pages/
│       ├── AdminProducts.tsx  # Updated admin interface
│       └── Products.tsx       # Updated product display
```

## Security Features

1. **Admin-Only Access**: Image upload requires admin authentication
2. **File Type Validation**: Only image files are accepted
3. **File Size Limits**: Maximum 5MB per image
4. **Image Format Validation**: Uses Pillow to verify image integrity
5. **Unique Filenames**: UUID-based naming prevents conflicts
6. **Path Traversal Protection**: Secure file serving

## Error Handling

### Backend Errors
- Invalid file type
- File too large (>5MB)
- Corrupted image files
- Authentication failures
- Server errors

### Frontend Errors
- Network connectivity issues
- Upload failures
- File validation errors
- Display errors for missing images

## Configuration

### File Upload Settings
- **Max File Size**: 5MB
- **Allowed Formats**: JPG, JPEG, PNG, GIF, WebP
- **Upload Directory**: `uploads/` (created automatically)
- **Image Serving**: Through `/upload/uploads/{filename}` endpoint

### Database Migration
Run the migration script to add the image_url column to existing databases:
```bash
python migrate_add_image_url.py
```

## Testing

### Manual Testing
1. Start the backend server: `python -m uvicorn app.main:app --reload`
2. Start the frontend: `cd frontend && npm run dev`
3. Login as admin
4. Navigate to Admin Products
5. Test image upload functionality
6. Verify images display on Products page

### Automated Testing
Run the test script to verify backend functionality:
```bash
python test_image_upload.py
```

## Future Enhancements

1. **Image Editing**: Add image cropping and resizing
2. **Multiple Images**: Support for multiple images per product
3. **Image Optimization**: Automatic image compression
4. **Cloud Storage**: Integration with cloud storage services
5. **Image CDN**: Content delivery network for better performance
6. **Bulk Upload**: Upload multiple images at once

## Troubleshooting

### Common Issues

1. **Upload Directory Not Found**:
   - The uploads directory is created automatically
   - Ensure the application has write permissions

2. **Image Not Displaying**:
   - Check if the image URL is correct
   - Verify the image file exists in the uploads directory
   - Check browser console for errors

3. **Upload Fails**:
   - Verify file type is supported
   - Check file size is under 5MB
   - Ensure admin authentication is valid

4. **Database Migration Issues**:
   - Run the migration script manually
   - Check database permissions
   - Verify SQLite database file exists

## API Endpoints

### POST /upload/image
Upload a product image (admin only)

**Request**:
- Content-Type: multipart/form-data
- Authorization: Bearer token required
- Body: file field with image file

**Response**:
```json
{
  "filename": "uuid.jpg",
  "url": "/upload/uploads/uuid.jpg"
}
```

### GET /upload/uploads/{filename}
Serve an uploaded image

**Response**:
- Content-Type: image/*
- Body: Image file data

## Dependencies

### Backend
- Pillow==10.4.0
- python-multipart (already included)
- FastAPI
- SQLAlchemy

### Frontend
- React
- TypeScript
- No additional dependencies required
