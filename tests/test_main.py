from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


def test_reset_db():
    response = client.post("/reset-db")
    assert response.status_code == 200
    assert "message" in response.json()

def test_reset_db_exception():
    with patch("app.main.Department.__table__.drop", side_effect=Exception("DB error")):
        response = client.post("/reset-db")
        assert response.status_code == 500
        assert "Error resetting DB" in response.json()["detail"]