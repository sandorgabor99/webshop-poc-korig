#!/usr/bin/env python3
"""
Migration script to add unique order_id field to the orders table.
Run this script to add order ID functionality to an existing database.
"""

import sqlite3
import uuid
from pathlib import Path

def migrate_add_order_id():
    """Add order_id field to the orders table"""
    
    # Get the database path
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found. Please run the main application first to create the database.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if order_id column already exists
        cursor.execute("PRAGMA table_info(orders)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'order_id' in columns:
            print("Order ID column already exists. Migration not needed.")
            return
        
        # Add order_id column
        cursor.execute("ALTER TABLE orders ADD COLUMN order_id TEXT")
        
        # Create index for order_id
        cursor.execute("CREATE INDEX idx_orders_order_id ON orders (order_id)")
        
        # Update existing orders to have a unique order_id
        cursor.execute("SELECT id FROM orders")
        orders = cursor.fetchall()
        
        for (order_id,) in orders:
            # Generate unique order ID
            unique_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            # Update the order with the unique order_id
            cursor.execute("UPDATE orders SET order_id = ? WHERE id = ?", (unique_id, order_id))
            print(f"Updated order {order_id} with order_id: {unique_id}")
        
        # Commit the changes
        conn.commit()
        print("✅ Order ID column added successfully!")
        print("✅ Order ID index created for better performance!")
        print("✅ Existing orders updated with unique order IDs!")
        
    except sqlite3.Error as e:
        print(f"❌ Error adding order_id column: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Starting order ID migration...")
    migrate_add_order_id()
    print("✅ Migration completed!")
