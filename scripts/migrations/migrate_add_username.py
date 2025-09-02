#!/usr/bin/env python3
"""
Migration script to add username field to the users table.
Run this script to add username functionality to an existing database.
"""

import sqlite3
import os
from pathlib import Path

def migrate_add_username():
    """Add username field to the users table"""
    
    # Get the database path
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found. Please run the main application first to create the database.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if username column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'username' in columns:
            print("Username column already exists. Migration not needed.")
            return
        
        # Add username column
        cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
        
        # Create index for username
        cursor.execute("CREATE INDEX idx_users_username ON users (username)")
        
        # Update existing users to have a username based on their email
        cursor.execute("SELECT id, email FROM users")
        users = cursor.fetchall()
        
        for user_id, email in users:
            # Extract username from email (part before @)
            username = email.split('@')[0]
            
            # Check if username already exists, if so add a number
            base_username = username
            counter = 1
            while True:
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if not cursor.fetchone():
                    break
                username = f"{base_username}{counter}"
                counter += 1
            
            # Update the user with the username
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
            print(f"Updated user {email} with username: {username}")
        
        # Commit the changes
        conn.commit()
        print("✅ Username column added successfully!")
        print("✅ Username index created for better performance!")
        print("✅ Existing users updated with usernames!")
        
    except sqlite3.Error as e:
        print(f"❌ Error adding username column: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Starting username migration...")
    migrate_add_username()
    print("✅ Migration completed!")
