#!/usr/bin/env python3
"""
Script to fix admin user's username if it's missing.
"""

import sqlite3
from pathlib import Path

def fix_admin_username():
    """Fix admin user's username"""
    
    # Get the database path
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found. Please run the main application first to create the database.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Find admin user
        cursor.execute("SELECT id, email, username FROM users WHERE email = 'admin@example.com'")
        admin_user = cursor.fetchone()
        
        if not admin_user:
            print("Admin user not found.")
            return
        
        user_id, email, username = admin_user
        
        if username:
            print(f"Admin user already has username: {username}")
            return
        
        # Set admin username
        admin_username = "admin"
        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (admin_username, user_id))
        conn.commit()
        print(f"Updated admin user with username: {admin_username}")
        
    except sqlite3.Error as e:
        print(f"❌ Error fixing admin username: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Fixing admin username...")
    fix_admin_username()
    print("✅ Admin username fix completed!")
