from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

BASE = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE / "templates"))

app = FastAPI(title="ECG Frontend (demo)")
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")

# Simple in-memory user store (demo only)
USERS = {"doctor": {}, "patient": {}}

def valid_role(r: str) -> bool:
    return r in ("doctor", "patient")

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
    username: str = Form(...), 
    password: str = Form(...),
    license: str = Form(None),
    specialization: str = Form(None),
    fullname: str = Form(None),
    dob: str = Form(None)
):
    if not valid_role(role):
        return RedirectResponse("/", status_code=303)
    
    if username in USERS[role]:
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "role": role, "error": "Username already exists"}
        )
    
    # Store user data based on role
    user_data = {"password": password}
    
    if role == "doctor":
        user_data["license"] = license
        user_data["specialization"] = specialization
    else:  # patient
        user_data["fullname"] = fullname
        user_data["dob"] = dob
    
    USERS[role][username] = user_data
    return RedirectResponse(f"/login/{role}?registered=1", status_code=303)


@app.get("/login/{role}")
def login_get(request: Request, role: str):
    if not valid_role(role):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "role": role, "registered": request.query_params.get("registered")}
    )


@app.post("/login/{role}")
async def login_post(
    request: Request, 
    role: str, 
    username: str = Form(...), 
    password: str = Form(...)
):
    if not valid_role(role):
        return RedirectResponse("/", status_code=303)
    
    user_data = USERS[role].get(username)
    
    if user_data and user_data.get("password") == password:
        return RedirectResponse(f"/session?role={role}&user={username}", status_code=303)
    
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "role": role, "error": "Invalid credentials"}
    )


@app.get("/session")
def session(request: Request, role: str = "", user: str = ""):
    if not valid_role(role) or not user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(
        "session.html", 
        {"request": request, "role": role, "user": user}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)