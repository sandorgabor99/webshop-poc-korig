#!/usr/bin/env python3
"""
Script to improve product images with more specific and accurate product images
"""

import sqlite3
from pathlib import Path

def improve_product_images():
    """Update product images with more specific and accurate product images"""
    
    # Get the database path
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔄 Improving product images with more specific images...")
        
        # More specific product images with better matching
        product_images = [
            # Smartphones
            ("iPhone 15 Pro", "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop&crop=center"),
            ("Samsung Galaxy S24", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&crop=center"),
            
            # Laptops
            ("MacBook Air M2", "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop&crop=center"),
            ("Dell XPS 13", "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&h=400&fit=crop&crop=center"),
            ("Microsoft Surface Pro 9", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop&crop=center"),
            
            # Tablets
            ("iPad Air", "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop&crop=center"),
            
            # Audio Equipment
            ("Sony WH-1000XM5", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&crop=center"),
            ("Bose QuietComfort 45", "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop&crop=center"),
            
            # Footwear
            ("Nike Air Max 270", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&crop=center"),
            
            # Cameras
            ("Canon EOS R6", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=400&fit=crop&crop=center"),
            ("GoPro Hero 11", "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400&h=400&fit=crop&crop=center"),
            
            # Smartwatches
            ("Apple Watch Series 9", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&crop=center"),
            
            # Gaming
            ("PlayStation 5", "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400&h=400&fit=crop&crop=center"),
            
            # E-readers
            ("Kindle Paperwhite", "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop&crop=center"),
            
            # Drones
            ("DJI Mini 3 Pro", "https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=400&h=400&fit=crop&crop=center"),
        ]
        
        # Update each product's image
        for product_name, image_url in product_images:
            cursor.execute(
                "UPDATE products SET image_url = ? WHERE name = ?",
                (image_url, product_name)
            )
            print(f"  ✅ Updated {product_name} with specific product image")
        
        # Commit changes
        conn.commit()
        print("✅ Product images improved successfully!")
        
        # Show final product list
        cursor.execute("SELECT name, image_url FROM products WHERE name IN (SELECT name FROM products WHERE name LIKE '%iPhone%' OR name LIKE '%MacBook%' OR name LIKE '%Samsung%' OR name LIKE '%iPad%' OR name LIKE '%Sony%' OR name LIKE '%Nike%' OR name LIKE '%Canon%' OR name LIKE '%Dell%' OR name LIKE '%Apple Watch%' OR name LIKE '%Bose%' OR name LIKE '%PlayStation%' OR name LIKE '%Microsoft%' OR name LIKE '%GoPro%' OR name LIKE '%Kindle%' OR name LIKE '%DJI%') ORDER BY name")
        products = cursor.fetchall()
        
        print(f"\n📦 Final product images ({len(products)} products):")
        for name, image_url in products:
            print(f"  📱 {name}")
        
    except sqlite3.Error as e:
        print(f"❌ Error improving product images: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    improve_product_images()
