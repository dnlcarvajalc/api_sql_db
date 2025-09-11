from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_hired_employees_by_quarter():
    response = client.get("/metrics/hired-employees?year=2021")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        item = response.json()[0]
        assert "department" in item
        assert "job" in item
        assert "Q1" in item
        assert "Q2" in item
        assert "Q3" in item
        assert "Q4" in item

def test_departments_above_mean():
    response = client.get("/metrics/departments-above-mean?year=2021")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        item = response.json()[0]
        assert "id" in item
        assert "department" in item
        assert "hired" in item

def test_hired_employees_by_quarter_sql_file_exception():
    with patch("app.routes.metrics.Path.read_text", side_effect=Exception("SQL file error")):
        response = client.get("/metrics/hired-employees?year=2021")
        assert response.status_code == 500
        assert "Error reading SQL file" in response.json()["detail"]

def test_hired_employees_by_quarter_db_exception():
    with patch("app.routes.metrics.Session.execute", side_effect=Exception("DB error")):
        response = client.get("/metrics/hired-employees?year=2021")
        assert response.status_code == 500
        assert "Error executing SQL query" in response.json()["detail"]

def test_departments_above_mean_sql_file_exception():
    with patch("app.routes.metrics.Path.read_text", side_effect=Exception("SQL file error")):
        response = client.get("/metrics/departments-above-mean?year=2021")
        assert response.status_code == 500
        assert "Error reading SQL file" in response.json()["detail"]

def test_departments_above_mean_db_exception():
    with patch("app.routes.metrics.Session.execute", side_effect=Exception("DB error")):
        response = client.get("/metrics/departments-above-mean?year=2021")
        assert response.status_code == 500
        assert "Error executing SQL query" in response.json()["detail"]
