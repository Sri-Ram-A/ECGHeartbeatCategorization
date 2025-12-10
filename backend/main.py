import subprocess
import sys
from pathlib import Path
from fastapi import FastAPI, Request, Form, Depends
from typing import Annotated
from sqlmodel import Session,select
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException,Body
import schemas
import models

BASE = Path(__file__).parent
app = FastAPI(title="ECGBackend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, etc.
    allow_headers=["*"],  # allow all headers
)
# SQLModel dependency for models
SessionDep = Annotated[Session, Depends(models.get_session)]

@app.on_event("startup")
def on_startup():
    models.create_db_and_tables()

def valid_role(role):
    return role in ("doctor","patient")

@app.get("/")
def index(request: Request):
    return {"Welcome" : "Explore my API Endpoints"}

@app.post("/api/register/{role}")
def register_post(role: str,session: SessionDep, payload: dict = Body(...)):
    # Validate role
    if not valid_role(role):
        raise HTTPException(status_code=400, detail="Invalid role")

    if role == "doctor":
        data = schemas.DoctorCreate(**payload)
        doctor = models.Doctor(
            full_name=data.full_name,
            phone_number=data.phone_number,
            license_number=payload.get("licenseNumber"),
            specialization=payload.get("specialization"),
            password=data.password
        )
        session.add(doctor)
        session.commit()
        session.refresh(doctor)
        return {"status": "success", "doctor_id": doctor.id}

    elif role == "patient":  
        data = schemas.PatientCreate(**payload)
        patient = models.Patient(
            full_name=data.full_name,
            phone_number=data.phone_number,
            password=data.password,
            dob=data.dob
        )
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return {"status": "success", "patient_id": patient.id}

    

@app.post("/api/login/{role}")
async def login_post(
    role: str,
    session: SessionDep,
    payload: dict = Body(...)
):
    # Validate role
    if not valid_role(role):
        raise HTTPException(status_code=400, detail="Invalid role")

    full_name = payload.get("full_name")
    password = payload.get("password")
    if not full_name or not password:
        raise HTTPException(status_code=400, detail="Missing login fields")
    # Fetch user from DB
    if role == "doctor":
        user = session.exec(
            select(models.Doctor).where(models.Doctor.full_name == full_name)
        ).first()
    elif role == "patient":
        user = session.exec(
            select(models.Patient).where(models.Patient.full_name == full_name)
        ).first()
    # Authentication check
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    # Login success
    return {
        "status": "success",
        "role": role,
        "user_id": user.id,
        "full_name": user.full_name,
    }

# @app.post("/start-stream")
# def start_stream():
#     """
#     Trigger the publisher script to send demo ECG data.
#     """
#     script_path = Path(__file__).parent / "publisher.py"
#     if not script_path.exists():
#         return {"error": "publisher.py not found"}
#     # Trigger MQTT publisher non-blocking
#     subprocess.Popen([sys.executable, str(script_path)])
#     return RedirectResponse("/session?role=patient&user=test", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
