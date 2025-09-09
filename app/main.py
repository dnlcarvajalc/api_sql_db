from fastapi import FastAPI, Depends, HTTPException, Query
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models.department import Department
import app.constants as constants

app = FastAPI(
    title=constants.API_TITLE,
    description=constants.API_DESCRIPTION,
    version=constants.API_VERSION
)

engine = create_engine(
    constants.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", summary="Root Endpoint", response_description="Welcome message")
def read_root():
    return {"message": "Welcome to the Database Migration API!"}

@app.get("/db-hello", summary="Database Hello", response_description="Database connection test message")
def db_hello():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'Hello from the DB!'"))
        message = result.scalar()
    return {"message": message}

department_column_names = [col.name for col in Department.__table__.columns]
@app.post("/upload/departments", summary="Upload departments CSV from disk")
async def upload_departments(
    db: Session = Depends(get_db),
    batch_size: int = Query(1000, gt=0, le=1000, description="Number of rows per transaction")
):
    try:
        df = pd.read_csv(constants.DEPARTMENTS_CSV_FILE, header=None, names=department_column_names)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")
    total_inserted = 0
    try:
        for start in range(0, len(df), batch_size):
            chunk = df.iloc[start:start + batch_size]
            departments = [Department(**row.to_dict()) for _, row in chunk.iterrows()]
            db.bulk_save_objects(departments)
            db.commit()
            total_inserted += len(departments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    return {"inserted": total_inserted, "batch_size": batch_size}

@app.post("/reset-db", summary="Reset the departments table")
def reset_db(db: Session = Depends(get_db)):
    try:
        Department.__table__.drop(engine)
        Department.__table__.create(engine)
        return {"message": "Departments table has been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting DB: {e}")