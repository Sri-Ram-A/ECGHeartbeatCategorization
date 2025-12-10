# schemas.py
from pydantic import BaseModel, Field, field_validator

class DoctorCreate(BaseModel):
    full_name: str = Field(..., min_length=3)
    phone_number: str | None = None
    password: str = Field(..., min_length=6)
    specialization: str | None = None
    license_number: str | None = None
    password: str = Field(..., min_length=6)

class PatientCreate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    dob: str | None = None
    password: str = Field(..., min_length=6)

    @field_validator("phone_number")
    def validate_phone(cls, v):
        if v and len(v) != 10:
            raise ValueError("Phone number must be 10 digits")
        return v

