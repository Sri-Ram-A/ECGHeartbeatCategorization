from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine
from datetime import datetime

sqlite_file_name = "ecg.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class Doctor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(index=True, unique=True)
    phone_number: str | None = None 
    license_number: str | None = None
    specialization: str | None = None
    password: str
    
class Patient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
    full_name: str | None = None
    phone_number: str | None = None 
    dob: str | None = None
    
class RecordingSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int
    patient_id: int
    started_at: datetime = Field(default_factory=datetime.now)
    stopped_at: Optional[datetime] = None
    verdict:str

class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(index=True, unique=True)
    registered_at: datetime = Field(default_factory=datetime.now)
    last_seen: Optional[datetime] = None

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session