#!/usr/bin/env python3
"""
Test script for image upload functionality
"""
import requests
import json
import os
from pathlib import Path

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_IMAGE_PATH = "test_image.jpg"

def create_test_image():
    """Create a simple test image if it doesn't exist"""
    if not os.path.exists(TEST_IMAGE_PATH):
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple test image
        img = Image.new('RGB', (200, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add some text
        try:
            font = ImageFont.load_default()
        except:
            font = None
            
        draw.text((50, 90), "Test Image", fill='black', font=font)
        draw.rectangle([20, 20, 180, 180], outline='black', width=2)
        
        img.save(TEST_IMAGE_PATH)
        print(f"✅ Created test image: {TEST_IMAGE_PATH}")

def test_image_upload():
    """Test the image upload endpoint"""
    print("🧪 Testing image upload functionality...")
    
    # First, create a test image
    create_test_image()
    
    # Test login to get admin token
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    
    try:
        # Login
        login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            return
            
        token_data = login_response.json()
        access_token = token_data["access_token"]
        print("✅ Login successful")
        
        # Test image upload
        headers = {"Authorization": f"Bearer {access_token}"}
        
        with open(TEST_IMAGE_PATH, "rb") as f:
            files = {"file": ("test_image.jpg", f, "image/jpeg")}
            upload_response = requests.post(
                f"{BASE_URL}/upload/image",
                headers=headers,
                files=files
            )
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            print(f"✅ Image upload successful!")
            print(f"   Filename: {result['filename']}")
            print(f"   URL: {result['url']}")
            
            # Test image retrieval
            image_response = requests.get(f"{BASE_URL}{result['url']}")
            if image_response.status_code == 200:
                print("✅ Image retrieval successful!")
            else:
                print(f"❌ Image retrieval failed: {image_response.status_code}")
                
        else:
            print(f"❌ Image upload failed: {upload_response.status_code}")
            print(f"   Response: {upload_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_image_upload()
