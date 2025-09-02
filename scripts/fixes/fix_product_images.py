#!/usr/bin/env python3
"""
Script to fix product images with relevant product URLs
"""

import sqlite3
from pathlib import Path

def fix_product_images():
    """Update product images with relevant product URLs"""
    
    # Get the database path
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔄 Updating product images with relevant images...")
        
        # Updated product images with relevant URLs
        product_images = [
            ("iPhone 15 Pro", "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop"),
            ("MacBook Air M2", "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop"),
            ("Samsung Galaxy S24", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop"),
            ("iPad Air", "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop"),
            ("Sony WH-1000XM5", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"),
            ("Nike Air Max 270", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop"),
            ("Canon EOS R6", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=400&fit=crop"),
            ("Dell XPS 13", "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&h=400&fit=crop"),
            ("Apple Watch Series 9", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop"),
            ("Bose QuietComfort 45", "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop"),
            ("PlayStation 5", "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400&h=400&fit=crop"),
            ("Microsoft Surface Pro 9", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop"),
            ("GoPro Hero 11", "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400&h=400&fit=crop"),
            ("Kindle Paperwhite", "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop"),
            ("DJI Mini 3 Pro", "https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=400&h=400&fit=crop"),
        ]
        
        # Update each product's image
        for product_name, image_url in product_images:
            cursor.execute(
                "UPDATE products SET image_url = ? WHERE name = ?",
                (image_url, product_name)
            )
            print(f"  ✅ Updated {product_name} with relevant image")
        
        # Commit changes
        conn.commit()
        print("✅ Product images updated successfully!")
        
        # Show updated products
        cursor.execute("SELECT name, image_url FROM products ORDER BY name")
        products = cursor.fetchall()
        
        print("\n📦 Updated products:")
        for name, image_url in products:
            print(f"  {name}: {image_url}")
        
    except sqlite3.Error as e:
        print(f"❌ Error updating product images: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_product_images()
