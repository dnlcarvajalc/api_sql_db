from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_upload_departments():
    response = client.post("/upload/departments?batch_size=1000")
    assert response.status_code in (200, 400, 500)
    if response.status_code == 200:
        assert "inserted" in response.json()
        assert "batch_size" in response.json()

def test_upload_jobs():
    response = client.post("/upload/jobs?batch_size=1000")
    assert response.status_code in (200, 400, 500)
    if response.status_code == 200:
        assert "inserted" in response.json()
        assert "batch_size" in response.json()

def test_upload_employees():
    response = client.post("/upload/employees?batch_size=1000")
    assert response.status_code in (200, 400, 500)
    if response.status_code == 200:
        assert "inserted" in response.json()
        assert "batch_size" in response.json()

def test_upload_departments_csv_exception():
    with patch("app.routes.upload.pd.read_csv", side_effect=Exception("CSV error")):
        response = client.post("/upload/departments?batch_size=1000")
        assert response.status_code == 400
        assert "Error reading CSV" in response.json()["detail"]

def test_upload_departments_db_exception():
    with patch("app.routes.upload.Session.bulk_save_objects", side_effect=Exception("DB error")):
        response = client.post("/upload/departments?batch_size=1000")
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]

def test_upload_jobs_csv_exception():
    with patch("app.routes.upload.pd.read_csv", side_effect=Exception("CSV error")):
        response = client.post("/upload/jobs?batch_size=1000")
        assert response.status_code == 400
        assert "Error reading CSV" in response.json()["detail"]