from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from app.db import engine, Base
from app.models.departments import Department
from app.models.jobs import Job
from app.models.employees import HiredEmployee
from app.routes.upload import router as upload_router
from app.routes.metrics import router as metric_router
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


@app.get("/", summary="Root Endpoint", response_description="Welcome message")
def read_root():
    return {"message": "Welcome to the Database Migration API!"}

@app.get("/db-hello", summary="Database Hello", response_description="Database connection test message")
def db_hello():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'Hello from the DB!'"))
        message = result.scalar()
    return {"message": message}

app.include_router(upload_router)
app.include_router(metric_router)

@app.post("/reset-db", summary="Reset all tables")
def reset_db():
    models = [Department, Job, HiredEmployee]
    try:
        for model in models:
            model.__table__.drop(engine)
            model.__table__.create(engine)
        return {"message": "All tables have been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting DB: {e}")