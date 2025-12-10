from pathlib import Path
from fastapi import FastAPI, Request, Form, Depends
from typing import Annotated
from sqlmodel import Session, select
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import models
import subprocess
import sys

BASE = Path(__file__).parent
TEMPLATE_DIR = str(BASE / "templates")
STATIC_DIR = str(BASE / "static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)
app = FastAPI(title="ECG")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# SQLModel dependency
SessionDep = Annotated[Session, Depends(models.get_session)]


def valid_role(r: str) -> bool:
    return r in ("doctor", "patient")

@app.on_event("startup")
def on_startup():
    models.create_db_and_tables()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register/{role}")
def register_get(request: Request, role: str):
    if not valid_role(role):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request, "role": role})

@app.post("/register/{role}")
async def register_post(
    request: Request,
    role: str,
    session: SessionDep,
    username: str = Form(...),
    password: str = Form(...),
    license: str = Form(None),
    phone: str = Form(None),
    specialization: str = Form(None),
    fullname: str = Form(None),
    dob: str = Form(None),
):
    if not valid_role(role):
        return RedirectResponse("/", status_code=303)

    # ---- Phone validation ----
    if not phone or not phone.isdigit() or len(phone) != 10:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "role": role, "error": "Phone number must be exactly 10 digits"},
        )

    # ---- Username exists? ----
    if role == "doctor":
        existing_user = session.exec(
            select(models.Doctor).where(models.Doctor.username == username)
        ).first()
    else:
        existing_user = session.exec(
            select(models.Patient).where(models.Patient.username == username)
        ).first()

    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "role": role, "error": "Username already exists"},
        )

    # ---- Create new user ----
    if role == "doctor":
        new_user = models.Doctor(
            username=username,
            password=password,
            license=license,
            specialization=specialization,
            phone=phone,
        )
    else:
        new_user = models.Patient(
            username=username,
            password=password,
            fullname=fullname,
            dob=dob,
            phone=phone,
        )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return RedirectResponse(f"/login/{role}?registered=1", status_code=303)

@app.get("/login/{role}")
def login_get(request: Request, role: str):
    if not valid_role(role):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "role": role, "registered": request.query_params.get("registered")},
    )


@app.post("/login/{role}")
async def login_post(
    request: Request,
    role: str,
    session: SessionDep,
    username: str = Form(...),
    password: str = Form(...),
):
    if not valid_role(role):
        return RedirectResponse("/", status_code=303)

    # ----- LOGIN USING DATABASE -----
    if role == "doctor":
        user = session.exec(select(models.Doctor).where(models.Doctor.username == username)).first()
    else:
        user = session.exec(select(models.Patient).where(models.Patient.username == username)).first()

    if not user or user.password != password:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "role": role, "error": "Invalid credentials"},
        )
    return RedirectResponse(f"/session?role={role}&user={username}", status_code=303)


@app.get("/session")
def session_page(request: Request, role: str = "", user: str = ""):
    if not valid_role(role) or not user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(
        "session.html", {"request": request, "role": role, "user": user}
    )

@app.post("/start-stream")
def start_stream():
    """
    Trigger the publisher script to send demo ECG data.
    """
    script_path = Path(__file__).parent / "publisher.py"
    if not script_path.exists():
        return {"error": "publisher.py not found"}
    # Trigger MQTT publisher non-blocking
    subprocess.Popen([sys.executable, str(script_path)])
    return RedirectResponse("/session?role=patient&user=test", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
