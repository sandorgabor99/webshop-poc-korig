import pytest
from fastapi import status


class TestProducts:
    def test_list_products_empty(self, client):
        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_products_with_data(self, client, test_product):
        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == test_product.name
        assert data[0]["price"] == test_product.price

    def test_get_product_success(self, client, test_product):
        response = client.get(f"/products/{test_product.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == test_product.name
        assert data["price"] == test_product.price

    def test_get_product_not_found(self, client):
        response = client.get("/products/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_product_admin_success(self, client, admin_headers):
        response = client.post("/products/", json={
            "name": "New Product",
            "description": "A new product",
            "price": 49.99,
            "stock": 5
        }, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "New Product"
        assert data["price"] == 49.99
        assert data["stock"] == 5

    def test_create_product_unauthorized(self, client):
        response = client.post("/products/", json={
            "name": "New Product",
            "description": "A new product",
            "price": 49.99,
            "stock": 5
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_product_user_not_admin(self, client, auth_headers):
        response = client.post("/products/", json={
            "name": "New Product",
            "description": "A new product",
            "price": 49.99,
            "stock": 5
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_product_admin_success(self, client, admin_headers, test_product):
        response = client.patch(f"/products/{test_product.id}", json={
            "name": "Updated Product",
            "price": 39.99
        }, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Product"
        assert data["price"] == 39.99
        assert data["description"] == test_product.description  # unchanged

    def test_update_product_not_found(self, client, admin_headers):
        response = client.patch("/products/999", json={
            "name": "Updated Product"
        }, headers=admin_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_product_unauthorized(self, client, test_product):
        response = client.patch(f"/products/{test_product.id}", json={
            "name": "Updated Product"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_product_admin_success(self, client, admin_headers, test_product):
        response = client.delete(f"/products/{test_product.id}", headers=admin_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_product_not_found(self, client, admin_headers):
        response = client.delete("/products/999", headers=admin_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_unauthorized(self, client, test_product):
        response = client.delete(f"/products/{test_product.id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
