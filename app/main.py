from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/db-hello")
def db_hello():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Hello from the DB!'"))
        message = result.scalar()
    return {"message": message}