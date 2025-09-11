from sqlalchemy import text
from app.db import engine, SessionLocal, get_db

def test_engine_connect():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1

def test_session_local():
    db = SessionLocal()
    assert db is not None
    db.close()

def test_get_db():
    gen = get_db()
    db = next(gen)
    assert db is not None
    try:
        next(gen)
    except StopIteration:
        pass
    finally:
        gen.close()