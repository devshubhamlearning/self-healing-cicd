import sys
import os
sys.path.insert(0, "/app")

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_divide():
    response = client.get("/divide?a=10&b=2")
    assert response.json()["result"] == 5

def test_divide_by_zero():
    # Intentionally failing to trigger self-heal
    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 200
