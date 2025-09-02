#!/usr/bin/env python3
"""
Script to populate usernames for existing users who don't have them yet.
"""

import sqlite3
from pathlib import Path

def populate_usernames():
    """Populate usernames for existing users"""
    
    # Get the database path
    db_path = Path("webshop.db")
    
    if not db_path.exists():
        print("Database file not found. Please run the main application first to create the database.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get all users without usernames
        cursor.execute("SELECT id, email FROM users WHERE username IS NULL OR username = ''")
        users = cursor.fetchall()
        
        if not users:
            print("All users already have usernames. No action needed.")
            return
        
        print(f"Found {len(users)} users without usernames. Populating...")
        
        for user_id, email in users:
            # Extract username from email (part before @)
            username = email.split('@')[0]
            
            # Check if username already exists, if so add a number
            base_username = username
            counter = 1
            while True:
                cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
                if not cursor.fetchone():
                    break
                username = f"{base_username}{counter}"
                counter += 1
            
            # Update the user with the username
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
            print(f"Updated user {email} with username: {username}")
        
        # Commit the changes
        conn.commit()
        print("✅ Usernames populated successfully!")
        
    except sqlite3.Error as e:
        print(f"❌ Error populating usernames: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Starting username population...")
    populate_usernames()
    print("✅ Username population completed!")
