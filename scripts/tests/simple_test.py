#!/usr/bin/env python3
"""
Simple test to verify authentication system
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_server():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Server status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("Server is not running. Please start the server first.")
        return False

def test_register():
    """Test user registration"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test@example.com",
        "username": "test",
        "password": "password123",
        "role": "CUSTOMER"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Register response: {response.status_code}")
        if response.status_code == 200:
            print(f"User created: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def test_login():
    """Test user login"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"Token received: {token[:20]}...")
            return token
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    return None

def main():
    print("=== Simple Authentication Test ===\n")
    
    if not test_server():
        return
    
    print("\n1. Testing registration...")
    test_register()
    
    print("\n2. Testing login...")
    token = test_login()
    
    if token:
        print("\n3. Testing /me endpoint...")
        url = f"{BASE_URL}/auth/me"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, headers=headers)
            print(f"/me response: {response.status_code}")
            if response.status_code == 200:
                print(f"User data: {response.json()}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    main()
