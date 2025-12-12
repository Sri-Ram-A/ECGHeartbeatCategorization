from fastapi import APIRouter, Body, HTTPException, Request, Depends
from sqlmodel import Session, select
from typing import Annotated
import models, schemas
from security import hash_password, verify_password

router = APIRouter(prefix="/api", tags=["HTTP API"])

SessionDep = Annotated[Session, Depends(models.get_session)]

def valid_role(role):
    return role in ("doctor", "patient")

@router.post("/register/{role}")
def register_post(role: str, session: SessionDep, payload: dict = Body(...)):
    if not valid_role(role):
        raise HTTPException(status_code=400, detail="Invalid role")

    # Extract fields early for reuse
    full_name = payload.get("full_name")
    phone_number = payload.get("phone_number")

    if not full_name or not phone_number:
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Check existing user (role-based)
    model = models.Doctor if role == "doctor" else models.Patient

    existing_user = session.exec(
        select(model).where(
            model.full_name == full_name,
            model.phone_number == phone_number
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with same name and phone number already exists"
        )

    # ——— Create Doctor ———
    if role == "doctor":
        data = schemas.DoctorCreate(**payload)
        doctor = models.Doctor(
            full_name=data.full_name,
            phone_number=data.phone_number,
            license_number=payload.get("licenseNumber"),
            specialization=payload.get("specialization"),
            password=hash_password(data.password)
        )
        session.add(doctor)
        session.commit()
        session.refresh(doctor)
        return {"status": "success", "doctor_id": doctor.id}

    # ——— Create Patient ———
    data = schemas.PatientCreate(**payload)
    patient = models.Patient(
        full_name=data.full_name,
        phone_number=data.phone_number,
        password=hash_password(data.password),
        dob=data.dob
    )
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return {"status": "success", "patient_id": patient.id}

@router.post("/login/{role}")
async def login_post(role: str, session: SessionDep, payload: dict = Body(...)):
    if not valid_role(role):
        raise HTTPException(status_code=400, detail="Invalid role")

    full_name = payload.get("full_name")
    password = payload.get("password")

    if not full_name or not password:
        raise HTTPException(status_code=400, detail="Missing login fields")

    # Fetch user
    query = models.Doctor if role == "doctor" else models.Patient
    user = session.exec(
        select(query).where(query.full_name == full_name)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "status": "success",
        "role": role,
        "user_id": user.id,
        "full_name": user.full_name,
    }

