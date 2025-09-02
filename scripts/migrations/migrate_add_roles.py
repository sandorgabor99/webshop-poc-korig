#!/usr/bin/env python3
"""
Migration script to add role-based user system
"""
import sqlite3
import os
from pathlib import Path

def migrate_database():
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found. Creating new database...")
        return
    
    print("Starting database migration...")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if role column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'role' not in columns:
            print("Adding role column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'CUSTOMER'")
            
            # Update existing admin users with correct enum values
            cursor.execute("UPDATE users SET role = 'ADMINISTRATOR' WHERE is_admin = 1")
            print("Updated existing admin users to have ADMINISTRATOR role")
            
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("Role column already exists. Updating values to match enum...")
            # Update existing values to match the enum
            cursor.execute("UPDATE users SET role = 'ADMINISTRATOR' WHERE role = 'administrator'")
            cursor.execute("UPDATE users SET role = 'CUSTOMER' WHERE role = 'customer'")
            print("Updated role values to match enum definition")
            
            conn.commit()
            print("Migration completed successfully!")
            
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
