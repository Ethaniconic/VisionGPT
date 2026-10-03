from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from app.services.image_services import validate_and_process_image
from app.models.vision import UploadResponse

router = APIRouter(prefix="/vision", tags=["Vision"])

@router.post("/upload", response_model=UploadResponse)
async def upload_image(image: UploadFile = File(...)):
    file_type = ["image/jpeg", "image/png", "image/jpg"]

    try:
        content = await image.read()
        result_data = validate_and_process_image(content, image.content_type)

        return UploadResponse(**result_data)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")