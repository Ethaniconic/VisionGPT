from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api import health, vision
from app.services.model_manager import model_manager

import logging

settings = get_settings()

app = FastAPI(
    title = settings.APP_NAME,
    debug = settings.DEBUG
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(health.router)
app.include_router(vision.router)

@app.on_event("startup")
async def startup_event():
    print(f"{settings.APP_NAME} started successfully")
    try:
        model_manager.load_models()
        logging.info(f"Models loaded successfully")
    except Exception as e:
        logging.error(f"Failed to load models: {e}")

    print(f"Docs available at http://localhost:8000/docs")