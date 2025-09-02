#!/usr/bin/env python3
"""
Migration script to add reviews table to the database.
Run this script to add the reviews functionality to an existing database.
"""

import sqlite3
import os
from pathlib import Path

def migrate_add_reviews():
    """Add reviews table to the database"""
    
    # Get the database path
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found. Please run the main application first to create the database.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if reviews table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reviews'")
        if cursor.fetchone():
            print("Reviews table already exists. Migration not needed.")
            return
        
        # Create reviews table
        cursor.execute("""
            CREATE TABLE reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX idx_reviews_user_id ON reviews (user_id)")
        cursor.execute("CREATE INDEX idx_reviews_product_id ON reviews (product_id)")
        cursor.execute("CREATE INDEX idx_reviews_created_at ON reviews (created_at)")
        
        # Commit the changes
        conn.commit()
        print("✅ Reviews table created successfully!")
        print("✅ Indexes created for better performance!")
        
    except sqlite3.Error as e:
        print(f"❌ Error creating reviews table: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Starting reviews table migration...")
    migrate_add_reviews()
    print("✅ Migration completed!")
