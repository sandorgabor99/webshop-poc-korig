#!/usr/bin/env python3
"""
Script to check database schema
"""

import sqlite3
from pathlib import Path

def check_schema():
    """Check database schema"""
    
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("📋 Database Schema:")
        
        # Check users table
        cursor.execute("PRAGMA table_info(users)")
        users_columns = cursor.fetchall()
        print("\n👥 Users table columns:")
        for col in users_columns:
            print(f"  {col[1]} ({col[2]}) - NOT NULL: {col[3]} - DEFAULT: {col[4]}")
        
        # Check products table
        cursor.execute("PRAGMA table_info(products)")
        products_columns = cursor.fetchall()
        print("\n📦 Products table columns:")
        for col in products_columns:
            print(f"  {col[1]} ({col[2]}) - NOT NULL: {col[3]} - DEFAULT: {col[4]}")
        
        # Check orders table
        cursor.execute("PRAGMA table_info(orders)")
        orders_columns = cursor.fetchall()
        print("\n🛒 Orders table columns:")
        for col in orders_columns:
            print(f"  {col[1]} ({col[2]}) - NOT NULL: {col[3]} - DEFAULT: {col[4]}")
        
        # Check current data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"\n📊 Current data:")
        print(f"  Users: {user_count}")
        
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"  Products: {product_count}")
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        print(f"  Orders: {order_count}")
        
    except sqlite3.Error as e:
        print(f"❌ Error checking schema: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_schema()
