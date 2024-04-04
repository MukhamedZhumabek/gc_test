import pytest

from sqlalchemy import select

from db.models import Store


@pytest.mark.asyncio
async def test_add_store(get_async_session):
    async with get_async_session() as session:
        store = Store()
        store.id = 1
        store.name = "Global Coffe Test"
        session.add(store)
        await session.commit()

        q = select(Store).where(Store.name == "Global Coffe Test")
        result = await session.execute(q)
        assert result.scalars().first().name == store.name


def test_create_product_success(client):
    headers = {"auth-token": "secret"}
    data = {
        "external_id": "1",
        "name": "Test Product",
        "description": {"key": "value"},
        "store_id": 1
    }
    response = client.post("/api/v1/product/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"


def test_create_product_invalid_body(client):
    headers = {"auth-token": "secret"}
    data = {
        "name": "Test Product",
        "description": {"key": "value"},
        "store_id": 1
    }
    response = client.post("/api/v1/product/", json=data, headers=headers)
    assert response.status_code == 422


def test_create_product_invalid_data(client):
    headers = {"auth-token": "secret"}
    data = {
        "external_id": "1",
        "name": "Test Product",
        "description": {"key": "value"},
        "store_id": 2
    }
    response = client.post("/api/v1/product/", json=data, headers=headers)
    assert response.status_code == 400


def test_create_product_unauthorized(client):
    headers = {"auth-token": "wrong"}
    data = {
        "external_id": "1",
        "name": "Test Product",
        "description": {"key": "value"},
        "store_id": 1
    }
    response = client.post("/api/v1/product/", json=data, headers=headers)
    assert response.status_code == 401


def test_read_product_success(client):
    headers = {"auth-token": "secret"}
    response = client.get("/api/v1/product/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["external_id"] == "1"


def test_read_product_not_found(client):
    headers = {"auth-token": "secret"}
    response = client.get("/api/v1/product/999", headers=headers)
    assert response.status_code == 404


async def test_update_product_success(client):
    headers = {"auth-token": "secret"}
    data = {
        "external_id": "1",
        "name": "Updated Product",
        "description": {"key": "updated_value"},
        "store_id": 1
    }
    response = client.put("/api/v1/product/", json=data, headers=headers)
    assert response.status_code == 200


async def test_update_product_invalid_data(client):
    headers = {"auth-token": "secret"}
    data = {
        "external_id": "1",
        "name": "Updated Product",
        "description": {"key": "updated_value"},
        "store_id": 2
    }
    response = client.put("/api/v1/product/", json=data, headers=headers)
    assert response.status_code == 400


async def test_update_product_invalid_body(client):
    headers = {"auth-token": "secret"}
    data = {
        "external_id": "1",
        "description": {"key": "updated_value"},
        "store_id": 2
    }
    response = client.put("/api/v1/product/", json=data, headers=headers)
    assert response.status_code == 422


def test_update_product_unauthorized(client):
    headers = {"auth-token": "wrong"}
    data = {
        "external_id": "1",
        "name": "Updated Product",
        "description": {"key": "updated_value"},
        "store_id": 1
    }
    response = client.put("/api/v1/product/", json=data, headers=headers)
    assert response.status_code == 401


def test_delete_product_success(client):
    headers = {"auth-token": "secret"}
    response = client.delete("/api/v1/product/1/1", headers=headers)
    assert response.status_code == 200


def test_delete_product_not_found(client):
    headers = {"auth-token": "secret"}
    response = client.delete("/api/v1/product/1/2", headers=headers)
    assert response.status_code == 404


def test_delete_product_unauthorized(client):
    headers = {"auth-token": "wrong"}
    response = client.delete("/api/v1/product/1/1", headers=headers)
    assert response.status_code == 401
