from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ocr_service import ocr_service
from app.models.vision import OCRResponse

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/extract", response_model=OCRResponse)
async def extract_text(image: UploadFile = File(...)):
    content = await image.read()

    try:
        result = ocr_service.extract_text(content)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")