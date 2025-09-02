#!/usr/bin/env python3
"""
Demonstration of the working authentication and role system
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_server():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"✅ Server is running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start with: python -m uvicorn app.main:app --reload")
        return False

def demo_registration():
    """Demonstrate user registration with roles"""
    print("\n=== User Registration Demo ===")
    
    # Register a customer
    customer_data = {
        "email": "customer@demo.com",
        "password": "password123",
        "role": "CUSTOMER"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=customer_data)
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Customer registered: {user['email']} (Role: {user['role']}, Is Admin: {user['is_admin']})")
    else:
        print(f"❌ Customer registration failed: {response.text}")
    
    # Register an administrator
    admin_data = {
        "email": "admin@demo.com",
        "password": "password123",
        "role": "ADMINISTRATOR"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=admin_data)
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Administrator registered: {user['email']} (Role: {user['role']}, Is Admin: {user['is_admin']})")
    else:
        print(f"❌ Administrator registration failed: {response.text}")

def demo_login():
    """Demonstrate user login and token generation"""
    print("\n=== User Login Demo ===")
    
    # Login as customer
    customer_login = {
        "username": "customer@demo.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=customer_login)
    if response.status_code == 200:
        token_data = response.json()
        customer_token = token_data["access_token"]
        print(f"✅ Customer login successful - Token: {customer_token[:20]}...")
    else:
        print(f"❌ Customer login failed: {response.text}")
        customer_token = None
    
    # Login as administrator
    admin_login = {
        "username": "admin@demo.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=admin_login)
    if response.status_code == 200:
        token_data = response.json()
        admin_token = token_data["access_token"]
        print(f"✅ Administrator login successful - Token: {admin_token[:20]}...")
    else:
        print(f"❌ Administrator login failed: {response.text}")
        admin_token = None
    
    return customer_token, admin_token

def demo_user_info(customer_token, admin_token):
    """Demonstrate getting user information"""
    print("\n=== User Information Demo ===")
    
    if customer_token:
        headers = {"Authorization": f"Bearer {customer_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Customer info: {user['email']} (Role: {user['role']}, Is Admin: {user['is_admin']})")
        else:
            print(f"❌ Failed to get customer info: {response.text}")
    
    if admin_token:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Administrator info: {user['email']} (Role: {user['role']}, Is Admin: {user['is_admin']})")
        else:
            print(f"❌ Failed to get administrator info: {response.text}")

def demo_role_based_access(customer_token, admin_token):
    """Demonstrate role-based access control"""
    print("\n=== Role-Based Access Control Demo ===")
    
    # Test admin-only endpoint with customer (should fail)
    if customer_token:
        headers = {"Authorization": f"Bearer {customer_token}"}
        response = requests.get(f"{BASE_URL}/auth/admin-only", headers=headers)
        if response.status_code == 403:
            print("✅ Customer correctly denied access to admin-only endpoint")
        else:
            print(f"❌ Customer access control failed: {response.status_code}")
    
    # Test admin-only endpoint with administrator (should succeed)
    if admin_token:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(f"{BASE_URL}/auth/admin-only", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Administrator can access admin-only endpoint: {data['message']}")
        else:
            print(f"❌ Administrator access control failed: {response.status_code}")

def demo_product_management(customer_token, admin_token):
    """Demonstrate product management with role-based access"""
    print("\n=== Product Management Demo ===")
    
    # Test customer trying to create product (should fail)
    if customer_token:
        headers = {"Authorization": f"Bearer {customer_token}"}
        product_data = {
            "name": "Customer Product",
            "description": "This should fail",
            "price": 99.99,
            "stock": 10
        }
        response = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
        if response.status_code == 403:
            print("✅ Customer correctly denied access to create products")
        else:
            print(f"❌ Customer product creation control failed: {response.status_code}")
    
    # Test administrator creating product (should succeed)
    if admin_token:
        headers = {"Authorization": f"Bearer {admin_token}"}
        product_data = {
            "name": "Admin Product",
            "description": "Created by administrator",
            "price": 149.99,
            "stock": 5
        }
        response = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Administrator successfully created product: {product['name']} (${product['price']})")
        else:
            print(f"❌ Administrator product creation failed: {response.status_code}")

def main():
    print("🚀 Authentication and Role System Demonstration")
    print("=" * 50)
    
    if not test_server():
        return
    
    # Run demonstrations
    demo_registration()
    customer_token, admin_token = demo_login()
    demo_user_info(customer_token, admin_token)
    demo_role_based_access(customer_token, admin_token)
    demo_product_management(customer_token, admin_token)
    
    print("\n" + "=" * 50)
    print("✅ Authentication and Role System Demo Complete!")
    print("\nKey Features Demonstrated:")
    print("• User registration with role selection (CUSTOMER/ADMINISTRATOR)")
    print("• JWT token-based authentication")
    print("• Role-based access control")
    print("• Admin-only endpoints")
    print("• Product management with role restrictions")

if __name__ == "__main__":
    main()
