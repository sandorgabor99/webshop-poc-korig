#!/usr/bin/env python3
"""
Script to populate the database with sample users and products.
This will create test data for the webshop application.
"""

import sqlite3
import uuid
from pathlib import Path
from datetime import datetime, timedelta
import random
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Password hashing function using bcrypt"""
    return pwd_context.hash(password)

def populate_sample_data():
    """Populate database with sample users and products"""
    
    # Get the database path
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found. Please run the main application first to create the database.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔄 Starting sample data population...")
        
        # Sample users data
        sample_users = [
            ("john.doe@example.com", "johndoe", "customer123"),
            ("jane.smith@example.com", "janesmith", "customer123"),
            ("mike.wilson@example.com", "mikewilson", "customer123"),
            ("sarah.jones@example.com", "sarahjones", "customer123"),
            ("david.brown@example.com", "davidbrown", "customer123"),
            ("emma.davis@example.com", "emmadavis", "customer123"),
            ("alex.taylor@example.com", "alextaylor", "customer123"),
            ("lisa.anderson@example.com", "lisaanderson", "customer123"),
            ("tom.martinez@example.com", "tommartinez", "customer123"),
            ("anna.garcia@example.com", "annagarcia", "customer123"),
        ]
        
        # Sample products data
        sample_products = [
            ("iPhone 15 Pro", "Latest iPhone with advanced camera system and A17 Pro chip", 999.99, 50, "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400"),
            ("MacBook Air M2", "Ultra-thin laptop with M2 chip and all-day battery life", 1199.99, 30, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400"),
            ("Samsung Galaxy S24", "Android flagship with AI features and excellent camera", 899.99, 45, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"),
            ("iPad Air", "Powerful tablet perfect for creativity and productivity", 599.99, 60, "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400"),
            ("Sony WH-1000XM5", "Premium noise-cancelling headphones with exceptional sound", 349.99, 25, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"),
            ("Nike Air Max 270", "Comfortable running shoes with Air Max technology", 129.99, 100, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"),
            ("Canon EOS R6", "Professional mirrorless camera with 4K video", 2499.99, 15, "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400"),
            ("Dell XPS 13", "Premium ultrabook with InfinityEdge display", 999.99, 35, "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400"),
            ("Apple Watch Series 9", "Advanced smartwatch with health monitoring", 399.99, 40, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"),
            ("Bose QuietComfort 45", "Comfortable wireless headphones with noise cancellation", 329.99, 30, "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400"),
            ("PlayStation 5", "Next-gen gaming console with lightning-fast loading", 499.99, 20, "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400"),
            ("Microsoft Surface Pro 9", "Versatile 2-in-1 laptop and tablet", 1099.99, 25, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"),
            ("GoPro Hero 11", "Action camera with 5.3K video and stabilization", 399.99, 50, "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400"),
            ("Kindle Paperwhite", "Waterproof e-reader with adjustable warm light", 139.99, 75, "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400"),
            ("DJI Mini 3 Pro", "Ultralight drone with 4K camera and obstacle avoidance", 759.99, 15, "https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=400"),
        ]
        
        # Check if users already exist
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'CUSTOMER'")
        existing_users = cursor.fetchone()[0]
        
        if existing_users >= 10:
            print("✅ Sample users already exist. Skipping user creation.")
        else:
            print(f"📝 Creating {len(sample_users)} sample users...")
            
            # Create users
            for email, username, password in sample_users:
                # Check if user already exists
                cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
                if cursor.fetchone():
                    continue
                
                # Hash password properly
                password_hash = hash_password(password)
                
                cursor.execute(
                    "INSERT INTO users (email, username, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
                    (email, username, password_hash, "CUSTOMER", datetime.now().isoformat())
                )
                print(f"  ✅ Created user: {username} ({email})")
        
        # Check if products already exist
        cursor.execute("SELECT COUNT(*) FROM products")
        existing_products = cursor.fetchone()[0]
        
        if existing_products >= 15:
            print("✅ Sample products already exist. Skipping product creation.")
        else:
            print(f"📦 Creating {len(sample_products)} sample products...")
            
            # Create products
            for name, description, price, stock, image_url in sample_products:
                # Check if product already exists
                cursor.execute("SELECT id FROM products WHERE name = ?", (name,))
                if cursor.fetchone():
                    continue
                
                cursor.execute(
                    "INSERT INTO products (name, description, price, stock, image_url, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, description, price, stock, image_url, datetime.now().isoformat())
                )
                print(f"  ✅ Created product: {name} (${price})")
        
        # Create some sample orders
        print("🛒 Creating sample orders...")
        
        # Get user IDs
        cursor.execute("SELECT id FROM users WHERE role = 'CUSTOMER' LIMIT 5")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        # Get product IDs
        cursor.execute("SELECT id, price FROM products LIMIT 10")
        products = cursor.fetchall()
        
        if user_ids and products:
            # Create 20 sample orders
            for order_num in range(1, 21):
                user_id = random.choice(user_ids)
                order_date = datetime.now() - timedelta(days=random.randint(1, 30))
                
                # Generate unique order ID
                order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                
                # Create order
                cursor.execute(
                    "INSERT INTO orders (order_id, user_id, total_amount, created_at) VALUES (?, ?, ?, ?)",
                    (order_id, user_id, 0, order_date.isoformat())
                )
                order_db_id = cursor.lastrowid
                
                # Add 1-3 items to each order
                num_items = random.randint(1, 3)
                total_amount = 0
                
                for _ in range(num_items):
                    product_id, price = random.choice(products)
                    quantity = random.randint(1, 3)
                    item_total = price * quantity
                    total_amount += item_total
                    
                    cursor.execute(
                        "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                        (order_db_id, product_id, quantity, price)
                    )
                
                # Update order total
                cursor.execute(
                    "UPDATE orders SET total_amount = ? WHERE id = ?",
                    (total_amount, order_db_id)
                )
                
                print(f"  ✅ Created order {order_id} for user {user_id} (${total_amount:.2f})")
        
        # Create some sample reviews
        print("⭐ Creating sample reviews...")
        
        # Get product IDs for reviews
        cursor.execute("SELECT id FROM products LIMIT 8")
        product_ids = [row[0] for row in cursor.fetchall()]
        
        if user_ids and product_ids:
            # Create 30 sample reviews
            for review_num in range(1, 31):
                user_id = random.choice(user_ids)
                product_id = random.choice(product_ids)
                rating = random.randint(3, 5)  # Mostly positive reviews
                review_date = datetime.now() - timedelta(days=random.randint(1, 60))
                
                # Sample feedback
                feedback_samples = [
                    "Great product, highly recommend!",
                    "Excellent quality and fast delivery.",
                    "Very satisfied with this purchase.",
                    "Good value for money.",
                    "Works perfectly as expected.",
                    "Love this product!",
                    "High quality and durable.",
                    "Exceeded my expectations.",
                    "Perfect for my needs.",
                    "Would buy again!",
                    "Amazing features and performance.",
                    "Great customer service too.",
                    "Best purchase I've made this year.",
                    "Highly recommend to others.",
                    "Excellent build quality.",
                ]
                
                feedback = random.choice(feedback_samples)
                
                cursor.execute(
                    "INSERT INTO reviews (user_id, product_id, rating, feedback, created_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, product_id, rating, feedback, review_date.isoformat())
                )
                
                print(f"  ✅ Created review: {rating}⭐ for product {product_id}")
        
        # Commit all changes
        conn.commit()
        
        print("✅ Sample data population completed successfully!")
        print(f"📊 Database now contains:")
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'CUSTOMER'")
        user_count = cursor.fetchone()[0]
        print(f"  👥 {user_count} customers")
        
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"  📦 {product_count} products")
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        print(f"  🛒 {order_count} orders")
        
        cursor.execute("SELECT COUNT(*) FROM reviews")
        review_count = cursor.fetchone()[0]
        print(f"  ⭐ {review_count} reviews")
        
        print("\n🎉 Your webshop is now populated with sample data!")
        print("💡 You can now test all features with realistic data.")
        
    except sqlite3.Error as e:
        print(f"❌ Error populating sample data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    populate_sample_data()
