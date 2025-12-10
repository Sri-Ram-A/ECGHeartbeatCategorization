from typing import Annotated ,Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime


sqlite_file_name = "ecg.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
from sqlmodel import Field, SQLModel

class Doctor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    license: str | None = None
    specialization: str | None = None
    phone: str | None = None 
    
class Patient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    fullname: str | None = None
    dob: str | None = None
    phone: str | None = None 
    
class RecordingSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    user_type: str  # 'doctor' or 'patient'
    started_at: datetime = Field(default_factory=datetime.now)
    stopped_at: Optional[datetime] = None
    is_active: bool = Field(default=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session