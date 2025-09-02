#!/usr/bin/env python3
"""
Fix database role values to match enum
"""
import sqlite3

def fix_database():
    print("Fixing database role values...")
    
    conn = sqlite3.connect('webshop.db')
    cursor = conn.cursor()
    
    try:
        # Show current state
        cursor.execute("SELECT id, email, role, is_admin FROM users")
        users = cursor.fetchall()
        print("Current users:")
        for user in users:
            print(f"ID: {user[0]}, Email: {user[1]}, Role: {user[2]}, Is Admin: {user[3]}")
        
        # Fix role values
        cursor.execute("UPDATE users SET role = 'ADMINISTRATOR' WHERE role = 'administrator'")
        cursor.execute("UPDATE users SET role = 'CUSTOMER' WHERE role = 'customer'")
        
        # Show updated state
        cursor.execute("SELECT id, email, role, is_admin FROM users")
        users = cursor.fetchall()
        print("\nUpdated users:")
        for user in users:
            print(f"ID: {user[0]}, Email: {user[1]}, Role: {user[2]}, Is Admin: {user[3]}")
        
        conn.commit()
        print("\nDatabase fixed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()


