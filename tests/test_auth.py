import pytest
from fastapi import status


class TestAuth:
    def test_register_success(self, client):
        response = client.post("/auth/register", json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpass123",
            "role": "CUSTOMER"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert data["role"] == "CUSTOMER"
        assert data["is_admin"] is False
        assert "id" in data
        assert "created_at" in data

    def test_register_duplicate_email(self, client, test_user):
        response = client.post("/auth/register", json={
            "email": test_user.email,
            "username": "differentuser",
            "password": "newpass123",
            "role": "CUSTOMER"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        response = client.post("/auth/register", json={
            "email": "invalid-email",
            "username": "testuser",
            "password": "newpass123",
            "role": "CUSTOMER"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_short_password(self, client):
        response = client.post("/auth/register", json={
            "email": "newuser@example.com",
            "username": "testuser",
            "password": "123",
            "role": "CUSTOMER"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_admin_success(self, client):
        response = client.post("/auth/register", json={
            "email": "newadmin@example.com",
            "username": "newadmin",
            "password": "newpass123",
            "role": "ADMINISTRATOR"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "newadmin@example.com"
        assert data["username"] == "newadmin"
        assert data["role"] == "ADMINISTRATOR"
        assert data["is_admin"] is True

    def test_login_success(self, client, test_user):
        response = client.post("/auth/login", data={
            "username": test_user.email,
            "password": "testpass123"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        response = client.post("/auth/login", data={
            "username": "nonexistent@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]

    def test_me_success(self, client, auth_headers):
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["role"] == "CUSTOMER"
        assert data["is_admin"] is False

    def test_me_unauthorized(self, client):
        response = client.get("/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_invalid_token(self, client):
        response = client.get("/auth/me", headers={"Authorization": "Bearer invalid"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_only_endpoint_customer(self, client, auth_headers):
        response = client.get("/auth/admin-only", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Administrator access required" in response.json()["detail"]

    def test_admin_only_endpoint_admin(self, client, admin_headers):
        response = client.get("/auth/admin-only", headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "user_id" in data
