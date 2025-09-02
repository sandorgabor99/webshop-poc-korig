#!/usr/bin/env python3
"""
Test script to verify authentication and role-based system
"""
import requests
import json
from typing import Dict, Any
import time

BASE_URL = "http://localhost:8000"

def test_register_user(email: str, password: str, role: str = "CUSTOMER") -> Dict[str, Any]:
    """Test user registration"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": email,
        "username": email.split('@')[0],  # Use email prefix as username
        "password": password,
        "role": role
    }
    
    response = requests.post(url, json=data)
    print(f"Register {email} ({role}): {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"  User ID: {user_data.get('id')}")
        print(f"  Email: {user_data.get('email')}")
        print(f"  Role: {user_data.get('role', 'N/A')}")
        print(f"  Is Admin: {user_data.get('is_admin', 'N/A')}")
        print(f"  Full response: {user_data}")
    else:
        print(f"  Error: {response.text}")
    
    return response.json() if response.status_code == 200 else None

def test_login(email: str, password: str) -> str:
    """Test user login and return access token"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": email,
        "password": password
    }
    
    response = requests.post(url, data=data)
    print(f"Login {email}: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"  Token received: {token[:20]}...")
        return token
    else:
        print(f"  Error: {response.text}")
        return None

def test_me_endpoint(token: str) -> Dict[str, Any]:
    """Test /me endpoint"""
    url = f"{BASE_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
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

def test_admin_endpoint(token: str) -> Dict[str, Any]:
    """Test admin-only endpoint"""
    url = f"{BASE_URL}/auth/admin-only"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"GET /admin-only: {response.status_code}")
    
    if response.status_code == 200:
        print(f"  Success: {response.json()}")
        return response.json()
    else:
        print(f"  Error: {response.text}")
        return None

def test_products_admin(token: str) -> Dict[str, Any]:
    """Test products admin endpoint"""
    url = f"{BASE_URL}/products/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 99.99,
        "stock": 10
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"POST /products/ (admin): {response.status_code}")
    
    if response.status_code == 200:
        print(f"  Product created: {response.json()['name']}")
        return response.json()
    else:
        print(f"  Error: {response.text}")
        return None

def main():
    print("=== Testing Authentication and Role System ===\n")
    
    # Generate unique timestamps for test data
    timestamp = int(time.time())
    
    # Test 1: Register a customer with unique email
    print("1. Testing customer registration...")
    customer_email = f"customer{timestamp}@test.com"
    customer_data = test_register_user(customer_email, "password123", "CUSTOMER")
    
    # Test 2: Register an administrator with unique email
    print("\n2. Testing administrator registration...")
    admin_email = f"admin{timestamp}@test.com"
    admin_data = test_register_user(admin_email, "password123", "ADMINISTRATOR")
    
    # Test 3: Login as customer
    print("\n3. Testing customer login...")
    customer_token = test_login(customer_email, "password123")
    
    # Test 4: Login as administrator
    print("\n4. Testing administrator login...")
    admin_token = test_login(admin_email, "password123")
    
    # Test 5: Test /me endpoint with customer
    print("\n5. Testing /me endpoint with customer...")
    if customer_token:
        test_me_endpoint(customer_token)
    
    # Test 6: Test /me endpoint with administrator
    print("\n6. Testing /me endpoint with administrator...")
    if admin_token:
        test_me_endpoint(admin_token)
    
    # Test 7: Test admin-only endpoint with customer (should fail)
    print("\n7. Testing admin-only endpoint with customer (should fail)...")
    if customer_token:
        test_admin_endpoint(customer_token)
    
    # Test 8: Test admin-only endpoint with administrator (should succeed)
    print("\n8. Testing admin-only endpoint with administrator (should succeed)...")
    if admin_token:
        test_admin_endpoint(admin_token)
    
    # Test 9: Test products admin endpoint with customer (should fail)
    print("\n9. Testing products admin endpoint with customer (should fail)...")
    if customer_token:
        test_products_admin(customer_token)
    
    # Test 10: Test products admin endpoint with administrator (should succeed)
    print("\n10. Testing products admin endpoint with administrator (should succeed)...")
    if admin_token:
        test_products_admin(admin_token)
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    main()
