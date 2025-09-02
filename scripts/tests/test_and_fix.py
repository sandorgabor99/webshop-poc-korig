#!/usr/bin/env python3
"""
Comprehensive test and fix script for authentication and roles
"""
import sqlite3
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def fix_database():
    """Fix the database role values"""
    print("=== Fixing Database ===")
    
    try:
        conn = sqlite3.connect('webshop.db')
        cursor = conn.cursor()
        
        # Show current state
        cursor.execute("SELECT id, email, role FROM users")
        users = cursor.fetchall()
        print("Current users:")
        for user in users:
            print(f"ID: {user[0]}, Email: {user[1]}, Role: {user[2]}")
        
        # Fix role values
        cursor.execute("UPDATE users SET role = 'ADMINISTRATOR' WHERE role = 'administrator'")
        cursor.execute("UPDATE users SET role = 'CUSTOMER' WHERE role = 'customer'")
        
        # Show updated state
        cursor.execute("SELECT id, email, role FROM users")
        users = cursor.fetchall()
        print("\nUpdated users:")
        for user in users:
            print(f"ID: {user[0]}, Email: {user[1]}, Role: {user[2]}")
        
        conn.commit()
        print("\nDatabase fixed successfully!")
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        return False

def test_server():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"Server status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("Server is not running. Please start the server first.")
        return False
    except Exception as e:
        print(f"Error testing server: {e}")
        return False

def test_register_user(email: str, password: str, role: str = "CUSTOMER"):
    """Test user registration"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": email,
        "username": email.split('@')[0],  # Use email prefix as username
        "password": password,
        "role": role
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Register {email} ({role}): {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"  User ID: {user_data.get('id')}")
            print(f"  Email: {user_data.get('email')}")
            print(f"  Role: {user_data.get('role')}")
            return user_data
        else:
            print(f"  Error: {response.text}")
            return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None

def test_login(email: str, password: str):
    """Test user login"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": email,
        "password": password
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        print(f"Login {email}: {response.status_code}")
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"  Token received: {token[:20]}...")
            return token
        else:
            print(f"  Error: {response.text}")
            return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None

def test_me_endpoint(token: str):
    """Test /me endpoint"""
    url = f"{BASE_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"GET /me: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"  User ID: {user_data['id']}")
            print(f"  Email: {user_data['email']}")
            print(f"  Role: {user_data['role']}")
            print(f"  Is Admin: {user_data['is_admin']}")
            return user_data
        else:
            print(f"  Error: {response.text}")
            return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None

def main():
    print("=== Authentication and Role System Test ===\n")
    
    # Step 1: Fix database
    if not fix_database():
        print("Failed to fix database. Exiting.")
        return
    
    # Step 2: Test server
    print("\n=== Testing Server ===")
    if not test_server():
        print("Please start the server with: python -m uvicorn app.main:app --reload")
        return
    
    # Step 3: Test registration and login
    print("\n=== Testing Authentication ===")
    
    # Test customer registration
    print("\n1. Testing customer registration...")
    customer_data = test_register_user("customer@test.com", "password123", "CUSTOMER")
    
    # Test administrator registration
    print("\n2. Testing administrator registration...")
    admin_data = test_register_user("admin@test.com", "password123", "ADMINISTRATOR")
    
    # Test customer login
    print("\n3. Testing customer login...")
    customer_token = test_login("customer@test.com", "password123")
    
    # Test administrator login
    print("\n4. Testing administrator login...")
    admin_token = test_login("admin@test.com", "password123")
    
    # Test /me endpoints
    if customer_token:
        print("\n5. Testing /me endpoint with customer...")
        test_me_endpoint(customer_token)
    
    if admin_token:
        print("\n6. Testing /me endpoint with administrator...")
        test_me_endpoint(admin_token)
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    main()
