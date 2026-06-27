import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from fastapi import FastAPI
from app.api.v1.endpoints.browser import router

app = FastAPI()
app.include_router(router, prefix="/browser")

client = TestClient(app)

def test_get_registry():
    response = client.get("/browser/registry")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "question_id" in data[0]

def test_search_questions():
    response = client.post("/browser/search", json={"query": "marriage"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["matched_domain_id"] == 7
    assert isinstance(data["question_ids"], list)

def test_search_questions_empty():
    response = client.post("/browser/search", json={"query": ""})
    assert response.status_code == 400

@patch('app.api.v1.endpoints.browser.preferences_manager')
def test_favorites_endpoints(mock_prefs):
    mock_prefs.list_favorites.return_value = [{"question_id": "7.1", "question_name": "Test"}]
    
    response = client.get("/browser/favorites")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    mock_prefs.add_favorite.return_value = {"question_id": "10.2"}
    response = client.post("/browser/favorites", json={"question_id": "10.2"})
    assert response.status_code == 200
    assert response.json()["question_id"] == "10.2"
    
    mock_prefs.remove_favorite.return_value = True
    response = client.delete("/browser/favorites/10.2")
    assert response.status_code == 200

@patch('app.api.v1.endpoints.browser.preferences_manager')
def test_recents_endpoints(mock_prefs):
    mock_prefs.list_recents.return_value = [{"question_id": "2.7", "question_name": "Test"}]
    
    response = client.get("/browser/recents")
    assert response.status_code == 200
    assert len(response.json()) == 1
