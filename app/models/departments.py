from sqlalchemy import Column, Integer, String
from app.db import Base


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)
