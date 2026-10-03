from fastapi import APIRouter
from app.services.model_manager import model_manager

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    info = model_manager.get_model_info()
    return {
        "status": "ok",
        "service": "VisionGPT",
        "model_status": info
    }