from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import pandas as pd
import app.constants as constants
from app.db import get_db
from app.models.departments import Department
from app.models.jobs import Job
from app.models.employees import HiredEmployee

router = APIRouter()


def upload_table_csv(model, csv_file_path: str, db: Session, batch_size: int):
    column_names = [col.name for col in model.__table__.columns]
    try:
        df = pd.read_csv(csv_file_path, header=None, names=column_names)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")
    total_inserted = 0
    try:
        for start in range(0, len(df), batch_size):
            chunk = df.iloc[start : start + batch_size]
            objects = [model(**row.to_dict()) for _, row in chunk.iterrows()]
            db.bulk_save_objects(objects)
            db.commit()
            total_inserted += len(objects)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    return {"inserted": total_inserted, "batch_size": batch_size}


@router.post("/upload/departments", summary="Upload departments CSV from disk")
async def upload_departments(
    db: Session = Depends(get_db), batch_size: int = Query(1000, gt=0, le=1000)
):
    return upload_table_csv(Department, constants.DEPARTMENTS_CSV_FILE, db, batch_size)


@router.post("/upload/jobs", summary="Upload jobs CSV from disk")
async def upload_jobs(
    db: Session = Depends(get_db), batch_size: int = Query(1000, gt=0, le=1000)
):
    return upload_table_csv(Job, constants.JOBS_CSV_FILE, db, batch_size)


@router.post("/upload/employees", summary="Upload employees CSV from disk")
async def upload_employees(
    db: Session = Depends(get_db), batch_size: int = Query(1000, gt=0, le=1000)
):
    return upload_table_csv(
        HiredEmployee, constants.HIRED_EMPLOYEES_CSV_FILE, db, batch_size
    )
