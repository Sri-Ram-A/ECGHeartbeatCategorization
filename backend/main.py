from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as http_router
from models import create_db_and_tables
from fastapi_mqtt import FastMQTT, MQTTConfig
import os, json
from loguru import logger
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))

app = FastAPI(title="ECG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB init
@app.on_event("startup")
def startup():
    create_db_and_tables()

# Routers
app.include_router(http_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
