from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pathlib import Path
from app.db import get_db

router = APIRouter()


@router.get(
    "/metrics/hired-employees",
    summary="Employees hired per job and department by quarter",
)
def hired_employees_by_quarter(
    year: int = Query(2021, description="Year to filter hires"),
    db: Session = Depends(get_db),
):
    sql_path = Path("app/sql/employees_hired_job.sql")
    try:
        query = sql_path.read_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading SQL file: {e}")
    try:
        result = db.execute(text(query), {"year": str(year)}).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing SQL query: {e}")
    return [
        {
            "department": row[0],
            "job": row[1],
            "Q1": row[2],
            "Q2": row[3],
            "Q3": row[4],
            "Q4": row[5],
        }
        for row in result
    ]


@router.get(
    "/metrics/departments-above-mean", summary="Departments hiring above mean in a year"
)
def departments_above_mean(
    year: int = Query(2021, description="Year to filter hires"),
    db: Session = Depends(get_db),
):
    sql_path = Path("app/sql/departments_above_mean.sql")
    try:
        query = sql_path.read_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading SQL file: {e}")
    try:
        result = db.execute(text(query), {"year": str(year)}).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing SQL query: {e}")
    return [
        {
            "id": row[0],
            "department": row[1],
            "hired": row[2],
        }
        for row in result
    ]
