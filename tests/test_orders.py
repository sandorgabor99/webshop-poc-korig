import pytest
from fastapi import status


class TestOrders:
    def test_create_order_success(self, client, auth_headers, test_product):
        response = client.post("/orders/", json={
            "items": [{
                "product_id": test_product.id,
                "quantity": 2
            }]
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_amount"] == test_product.price * 2
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == test_product.id
        assert data["items"][0]["quantity"] == 2

    def test_create_order_unauthorized(self, client, test_product):
        response = client.post("/orders/", json={
            "items": [{
                "product_id": test_product.id,
                "quantity": 2
            }]
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_empty_items(self, client, auth_headers):
        response = client.post("/orders/", json={
            "items": []
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "No items in order" in response.json()["detail"]

    def test_create_order_product_not_found(self, client, auth_headers):
        response = client.post("/orders/", json={
            "items": [{
                "product_id": 999,
                "quantity": 2
            }]
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_create_order_insufficient_stock(self, client, auth_headers, test_product):
        response = client.post("/orders/", json={
            "items": [{
                "product_id": test_product.id,
                "quantity": test_product.stock + 1
            }]
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient stock" in response.json()["detail"]

    def test_create_order_multiple_items(self, client, auth_headers, test_product, db_session):
        # Create second product
        from app.models import Product
        product2 = Product(
            name="Product 2",
            description="Second product",
            price=19.99,
            stock=5
        )
        db_session.add(product2)
        db_session.commit()

        response = client.post("/orders/", json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 1
                },
                {
                    "product_id": product2.id,
                    "quantity": 2
                }
            ]
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        expected_total = test_product.price * 1 + product2.price * 2
        assert data["total_amount"] == expected_total
        assert len(data["items"]) == 2

    def test_list_my_orders_empty(self, client, auth_headers):
        response = client.get("/orders/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_my_orders_with_data(self, client, auth_headers, test_product):
        # Create an order first
        client.post("/orders/", json={
            "items": [{
                "product_id": test_product.id,
                "quantity": 1
            }]
        }, headers=auth_headers)

        response = client.get("/orders/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["total_amount"] == test_product.price
        assert len(data[0]["items"]) == 1

    def test_list_my_orders_unauthorized(self, client):
        response = client.get("/orders/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_reduces_stock(self, client, auth_headers, test_product, db_session):
        initial_stock = test_product.stock
        response = client.post("/orders/", json={
            "items": [{
                "product_id": test_product.id,
                "quantity": 2
            }]
        }, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK

        # Check stock was reduced
        db_session.refresh(test_product)
        assert test_product.stock == initial_stock - 2
