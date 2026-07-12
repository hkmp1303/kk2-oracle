from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    r = client.get("/")
    assert r.status_code == 404

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_ai_ask():
    r = client.post("/ai/ask")
    assert r.status_code == 422

def test_data_upload():
    r = client.post("/data/upload")
    assert r.status_code == 422

def test_data_stats():
    r = client.get("/data/stats")
    assert r.status_code == 412
