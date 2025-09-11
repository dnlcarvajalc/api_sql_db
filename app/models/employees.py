from sqlalchemy import Column, Integer, String
from app.db import Base


class HiredEmployee(Base):
    __tablename__ = "hired_employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    datetime = Column(String, index=True)
    department_id = Column(Integer, index=True)
    job_id = Column(Integer, index=True)
