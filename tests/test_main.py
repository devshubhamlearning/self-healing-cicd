from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
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
    # This will FAIL - intentional to trigger self-healing
    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 200
