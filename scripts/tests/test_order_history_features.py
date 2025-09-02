#!/usr/bin/env python3
"""
Test script for Order History and Customer Management features
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"
CUSTOMER_EMAIL = "john.doe@example.com"
CUSTOMER_PASSWORD = "customer123"

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("🔐 Testing Authentication Endpoints...")
    
    # Test login
    login_data = {
        "username": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Admin login successful")
        return token
    else:
        print(f"❌ Admin login failed: {response.text}")
        return None

def test_order_history_endpoints(token):
    """Test order history endpoints"""
    print("\n📋 Testing Order History Endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test detailed orders
    response = requests.get(f"{BASE_URL}/orders/detailed", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        print(f"✅ Detailed orders endpoint working - Found {len(orders)} orders")
    else:
        print(f"❌ Detailed orders endpoint failed: {response.text}")
    
    # Test order summary
    response = requests.get(f"{BASE_URL}/orders/summary", headers=headers)
    if response.status_code == 200:
        summary = response.json()
        print(f"✅ Order summary endpoint working - Total orders: {summary.get('total_orders', 0)}")
    else:
        print(f"❌ Order summary endpoint failed: {response.text}")
    
    # Test specific order details
    if orders:
        first_order_id = orders[0]["id"]
        response = requests.get(f"{BASE_URL}/orders/{first_order_id}", headers=headers)
        if response.status_code == 200:
            print(f"✅ Specific order details endpoint working")
        else:
            print(f"❌ Specific order details endpoint failed: {response.text}")

def test_customer_management_endpoints(token):
    """Test customer management endpoints"""
    print("\n👥 Testing Customer Management Endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test list customers
    response = requests.get(f"{BASE_URL}/customers/", headers=headers)
    if response.status_code == 200:
        customers = response.json()
        print(f"✅ List customers endpoint working - Found {len(customers)} customers")
    else:
        print(f"❌ List customers endpoint failed: {response.text}")
    
    # Test customer details
    if customers:
        first_customer_id = customers[0]["id"]
        response = requests.get(f"{BASE_URL}/customers/{first_customer_id}", headers=headers)
        if response.status_code == 200:
            print(f"✅ Customer details endpoint working")
        else:
            print(f"❌ Customer details endpoint failed: {response.text}")
        
        # Test customer order summary
        response = requests.get(f"{BASE_URL}/customers/{first_customer_id}/summary", headers=headers)
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Customer order summary endpoint working")
        else:
            print(f"❌ Customer order summary endpoint failed: {response.text}")

def test_admin_order_endpoints(token):
    """Test admin order endpoints"""
    print("\n📊 Testing Admin Order Endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test all orders
    response = requests.get(f"{BASE_URL}/orders/admin/all", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        print(f"✅ Admin all orders endpoint working - Found {len(orders)} orders")
    else:
        print(f"❌ Admin all orders endpoint failed: {response.text}")
    
    # Test customer orders
    response = requests.get(f"{BASE_URL}/customers/", headers=headers)
    if response.status_code == 200:
        customers = response.json()
        if customers:
            first_customer_id = customers[0]["id"]
            response = requests.get(f"{BASE_URL}/orders/admin/customer/{first_customer_id}", headers=headers)
            if response.status_code == 200:
                customer_orders = response.json()
                print(f"✅ Admin customer orders endpoint working - Found {len(customer_orders)} orders for customer")
            else:
                print(f"❌ Admin customer orders endpoint failed: {response.text}")

def test_error_handling():
    """Test error handling"""
    print("\n🚫 Testing Error Handling...")
    
    # Test unauthorized access
    response = requests.get(f"{BASE_URL}/orders/detailed")
    if response.status_code == 401:
        print("✅ Unauthorized access properly blocked")
    else:
        print(f"❌ Unauthorized access not properly handled: {response.status_code}")
    
    # Test admin-only endpoint without admin token
    customer_token = test_customer_login()
    if customer_token:
        headers = {"Authorization": f"Bearer {customer_token}"}
        response = requests.get(f"{BASE_URL}/customers/", headers=headers)
        if response.status_code == 403:
            print("✅ Admin-only endpoints properly protected")
        else:
            print(f"❌ Admin-only endpoints not properly protected: {response.status_code}")

def test_customer_login():
    """Test customer login"""
    login_data = {
        "username": CUSTOMER_EMAIL,
        "password": CUSTOMER_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Customer login successful")
        return token
    else:
        print(f"❌ Customer login failed: {response.text}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing Order History and Customer Management Features")
    print("=" * 60)
    
    # Test authentication
    admin_token = test_auth_endpoints()
    if not admin_token:
        print("❌ Cannot proceed without admin token")
        return
    
    # Test order history endpoints
    test_order_history_endpoints(admin_token)
    
    # Test customer management endpoints
    test_customer_management_endpoints(admin_token)
    
    # Test admin order endpoints
    test_admin_order_endpoints(admin_token)
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("✅ Testing completed!")

if __name__ == "__main__":
    main()
