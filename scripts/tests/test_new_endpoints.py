#!/usr/bin/env python3
"""
Comprehensive test script for new Order History and Customer Management endpoints
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

class APITester:
    def __init__(self):
        self.admin_token = None
        self.test_results = []
    
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} {test_name}"
        if details:
            result += f" - {details}"
        print(result)
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def setup_auth(self):
        """Setup authentication"""
        print("🔐 Setting up authentication...")
        
        login_data = {
            "username": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "grant_type": "password",
            "scope": "",
            "client_id": "",
            "client_secret": ""
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            self.admin_token = response.json()["access_token"]
            self.log_test("Admin Authentication", True, "Token obtained successfully")
            return True
        else:
            self.log_test("Admin Authentication", False, f"Failed: {response.text}")
            return False
    
    def get_headers(self):
        """Get headers with authentication"""
        return {"Authorization": f"Bearer {self.admin_token}"}
    
    def test_order_history_endpoints(self):
        """Test order history endpoints"""
        print("\n📋 Testing Order History Endpoints...")
        
        # Test detailed orders
        response = requests.get(f"{BASE_URL}/orders/detailed", headers=self.get_headers())
        success = response.status_code == 200
        orders = response.json() if success else []
        self.log_test("GET /orders/detailed", success, f"Found {len(orders)} orders")
        
        # Test order summary
        response = requests.get(f"{BASE_URL}/orders/summary", headers=self.get_headers())
        success = response.status_code == 200
        if success:
            summary = response.json()
            total_orders = summary.get('total_orders', 0)
            total_spent = summary.get('total_spent', 0)
            self.log_test("GET /orders/summary", True, f"Total: {total_orders} orders, ${total_spent:.2f} spent")
        else:
            self.log_test("GET /orders/summary", False, f"Failed: {response.text}")
        
        # Test specific order details
        if orders:
            first_order_id = orders[0]["id"]
            response = requests.get(f"{BASE_URL}/orders/{first_order_id}", headers=self.get_headers())
            success = response.status_code == 200
            self.log_test(f"GET /orders/{first_order_id}", success, "Order details retrieved")
        
        # Test unauthorized access
        response = requests.get(f"{BASE_URL}/orders/detailed")
        self.log_test("Unauthorized Access Protection", response.status_code == 401, "Properly blocked")
    
    def test_customer_management_endpoints(self):
        """Test customer management endpoints"""
        print("\n👥 Testing Customer Management Endpoints...")
        
        # Test list customers
        response = requests.get(f"{BASE_URL}/customers/", headers=self.get_headers())
        success = response.status_code == 200
        customers = response.json() if success else []
        self.log_test("GET /customers/", success, f"Found {len(customers)} customers")
        
        # Test customer details
        if customers:
            first_customer_id = customers[0]["id"]
            response = requests.get(f"{BASE_URL}/customers/{first_customer_id}", headers=self.get_headers())
            success = response.status_code == 200
            if success:
                customer = response.json()
                self.log_test(f"GET /customers/{first_customer_id}", True, f"Customer: {customer.get('email', 'N/A')}")
            else:
                self.log_test(f"GET /customers/{first_customer_id}", False, f"Failed: {response.text}")
            
            # Test customer order summary
            response = requests.get(f"{BASE_URL}/customers/{first_customer_id}/summary", headers=self.get_headers())
            success = response.status_code == 200
            if success:
                summary = response.json()
                total_orders = summary.get('total_orders', 0)
                total_spent = summary.get('total_spent', 0)
                self.log_test(f"GET /customers/{first_customer_id}/summary", True, f"Orders: {total_orders}, Spent: ${total_spent:.2f}")
            else:
                self.log_test(f"GET /customers/{first_customer_id}/summary", False, f"Failed: {response.text}")
        
        # Test unauthorized access
        response = requests.get(f"{BASE_URL}/customers/")
        self.log_test("Customer Management Authorization", response.status_code == 401, "Properly blocked")
    
    def test_admin_order_endpoints(self):
        """Test admin order endpoints"""
        print("\n📊 Testing Admin Order Endpoints...")
        
        # Test all orders
        response = requests.get(f"{BASE_URL}/orders/admin/all", headers=self.get_headers())
        success = response.status_code == 200
        orders = response.json() if success else []
        self.log_test("GET /orders/admin/all", success, f"Found {len(orders)} orders from all customers")
        
        # Test customer orders
        response = requests.get(f"{BASE_URL}/customers/", headers=self.get_headers())
        if response.status_code == 200:
            customers = response.json()
            if customers:
                first_customer_id = customers[0]["id"]
                response = requests.get(f"{BASE_URL}/orders/admin/customer/{first_customer_id}", headers=self.get_headers())
                success = response.status_code == 200
                customer_orders = response.json() if success else []
                self.log_test(f"GET /orders/admin/customer/{first_customer_id}", success, f"Found {len(customer_orders)} orders for customer")
        
        # Test pagination
        response = requests.get(f"{BASE_URL}/orders/admin/all?skip=0&limit=10", headers=self.get_headers())
        success = response.status_code == 200
        self.log_test("Admin Orders Pagination", success, "Pagination parameters accepted")
        
        # Test unauthorized access
        response = requests.get(f"{BASE_URL}/orders/admin/all")
        self.log_test("Admin Orders Authorization", response.status_code == 401, "Properly blocked")
    
    def test_data_integrity(self):
        """Test data integrity and consistency"""
        print("\n🔍 Testing Data Integrity...")
        
        # Test order summary consistency
        response = requests.get(f"{BASE_URL}/orders/summary", headers=self.get_headers())
        if response.status_code == 200:
            summary = response.json()
            response2 = requests.get(f"{BASE_URL}/orders/detailed", headers=self.get_headers())
            if response2.status_code == 200:
                orders = response2.json()
                actual_count = len(orders)
                summary_count = summary.get('total_orders', 0)
                consistent = actual_count == summary_count
                self.log_test("Order Count Consistency", consistent, f"Summary: {summary_count}, Actual: {actual_count}")
        
        # Test customer data consistency
        response = requests.get(f"{BASE_URL}/customers/", headers=self.get_headers())
        if response.status_code == 200:
            customers = response.json()
            response2 = requests.get(f"{BASE_URL}/orders/admin/all", headers=self.get_headers())
            if response2.status_code == 200:
                all_orders = response2.json()
                # Check if all orders have valid customer IDs
                all_customer_ids = {customer['id'] for customer in customers}
                order_customer_ids = {order['user']['id'] for order in all_orders}
                valid_customers = order_customer_ids.issubset(all_customer_ids)
                self.log_test("Customer ID Consistency", valid_customers, f"All order customers exist")
    
    def test_response_format(self):
        """Test response format and structure"""
        print("\n📄 Testing Response Format...")
        
        # Test order detailed response format
        response = requests.get(f"{BASE_URL}/orders/detailed", headers=self.get_headers())
        if response.status_code == 200:
            orders = response.json()
            if orders:
                order = orders[0]
                required_fields = ['id', 'total_amount', 'created_at', 'items', 'user']
                has_required_fields = all(field in order for field in required_fields)
                self.log_test("Order Response Format", has_required_fields, "Contains all required fields")
                
                # Test item format
                if order['items']:
                    item = order['items'][0]
                    item_fields = ['id', 'product_id', 'quantity', 'unit_price', 'product']
                    has_item_fields = all(field in item for field in item_fields)
                    self.log_test("Order Item Format", has_item_fields, "Contains all required item fields")
        
        # Test customer response format
        response = requests.get(f"{BASE_URL}/customers/", headers=self.get_headers())
        if response.status_code == 200:
            customers = response.json()
            if customers:
                customer = customers[0]
                required_fields = ['id', 'email', 'role', 'is_admin', 'created_at', 'order_count', 'total_spent']
                has_required_fields = all(field in customer for field in required_fields)
                self.log_test("Customer Response Format", has_required_fields, "Contains all required fields")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Comprehensive API Testing for Order History and Customer Management")
        print("=" * 70)
        
        # Setup authentication
        if not self.setup_auth():
            print("❌ Cannot proceed without authentication")
            return
        
        # Run all test suites
        self.test_order_history_endpoints()
        self.test_customer_management_endpoints()
        self.test_admin_order_endpoints()
        self.test_data_integrity()
        self.test_response_format()
        
        # Summary
        print("\n" + "=" * 70)
        print("📋 Test Summary:")
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
        
        print("\n🎉 Testing completed!")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
