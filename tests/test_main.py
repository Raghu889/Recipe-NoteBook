import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine, SessionLocal
from sqlalchemy.orm import Session

# Create a new database for testing
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def user1_token():
    """Register and login first user"""
    client.post("/api/auth/register", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "pass123"
    })
    resp = client.post("/api/auth/login", data={
        "username": "user1@example.com",
        "password": "pass123"
    })
    return resp.json()["access_token"]


@pytest.fixture(scope="module")
def user2_token():
    """Register and login second user"""
    client.post("/api/auth/register", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "pass123"
    })
    resp = client.post("/api/auth/login", data={
        "username": "user2@example.com",
        "password": "pass123"
    })
    return resp.json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_recipe_user1(user1_token):
    resp = client.post("/api/recipe/", json={
        "title": "Pasta",
        "ingredients": ["noodles", "tomato"],
        "instructions": "Boil pasta and add sauce",
        "tags": ["italian"]
    }, headers=auth_header(user1_token))
    assert resp.status_code == 200
    assert resp.json()["title"] == "Pasta"
    global recipe1_id
    recipe1_id = resp.json()["id"]


def test_get_all_recipes():
    resp = client.get("/api/recipe/")
    assert resp.status_code == 200
    assert any(r["title"] == "Pasta" for r in resp.json())


def test_cannot_update_other_users_recipe(user2_token):
    resp = client.put(f"/api/recipe/{recipe1_id}", json={
        "title": "Updated Pasta"
    }, headers=auth_header(user2_token))
    assert resp.status_code == 403


def test_update_recipe_user1(user1_token):
    resp = client.put(f"/api/recipe/{recipe1_id}", json={
        "title": "Updated Pasta"
    }, headers=auth_header(user1_token))
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Pasta"


def test_owner_cannot_rate_their_own_recipe(user1_token):
    resp = client.post(f"/api/recipe/{recipe1_id}/rate", json={
        "rate": 5
    }, headers=auth_header(user1_token))
    assert resp.status_code == 403


def test_user2_rates_recipe(user2_token):
    resp = client.post(f"/api/recipe/{recipe1_id}/rate", json={
        "rate": 4
    }, headers=auth_header(user2_token))
    assert resp.status_code == 200
    assert resp.json()["rating"] == 4


def test_user2_cannot_rate_twice(user2_token):
    resp = client.post(f"/api/recipe/{recipe1_id}/rate", json={
        "rate": 3
    }, headers=auth_header(user2_token))
    assert resp.status_code == 400


def test_user1_cannot_save_own_recipe(user1_token):
    resp = client.post(f"/api/recipe/{recipe1_id}/save", headers=auth_header(user1_token))
    assert resp.status_code == 403


def test_user2_saves_recipe(user2_token):
    resp = client.post(f"/api/recipe/{recipe1_id}/save", headers=auth_header(user2_token))
    assert resp.status_code == 200
    assert resp.json()["recipe_id"] == recipe1_id


def test_user2_cannot_save_twice(user2_token):
    resp = client.post(f"/api/recipe/{recipe1_id}/save", headers=auth_header(user2_token))
    assert resp.status_code == 400


def test_get_saved_recipes(user2_token):
    resp = client.get("/api/recipe/user/save", headers=auth_header(user2_token))
    assert resp.status_code == 200
    assert any(r["id"] == recipe1_id for r in resp.json())


def test_unsave_recipe_user2(user2_token):
    resp = client.delete(f"/api/recipe/{recipe1_id}/unsave", headers=auth_header(user2_token))
    assert resp.status_code == 200
    assert resp.json()["detail"] == "Recipe unsaved successfully."


def test_search_by_name():
    resp = client.get("/api/recipe/user/search", params={"name": "Updated"})
    assert resp.status_code == 200
    assert any("Updated Pasta" in r["title"] for r in resp.json())


def test_delete_other_user_recipe(user2_token):
    resp = client.delete(f"/api/recipe/{recipe1_id}", headers=auth_header(user2_token))
    assert resp.status_code == 403


def test_user1_deletes_own_recipe(user1_token):
    resp = client.delete(f"/api/recipe/{recipe1_id}", headers=auth_header(user1_token))
    assert resp.status_code == 204
