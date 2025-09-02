#!/usr/bin/env python3
"""
Migration script to add image_url column to products table
"""
import sqlite3
import os

def migrate_database():
    db_path = "webshop.db"
    
    if not os.path.exists(db_path):
        print("Database file not found. Creating new database...")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if image_url column already exists
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if "image_url" not in columns:
            print("Adding image_url column to products table...")
            cursor.execute("ALTER TABLE products ADD COLUMN image_url TEXT")
            conn.commit()
            print("✅ Migration completed successfully!")
        else:
            print("✅ image_url column already exists. No migration needed.")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
