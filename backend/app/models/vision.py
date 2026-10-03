from typing import Optional
from pydantic import BaseModel

class UploadResponse(BaseModel):
    """
    This will be the response the user may get after the image upload is done.
    """
    success: bool
    message: str
    image_id: Optional[str] = None
    width: int
    height: int
    format: Optional[str] = None
    img_format: Optional[str] = None

class ValidationError(BaseModel):
    """
    This will be the primary structure of how the Validation Error for the images will look like.
    """
    error: str
    detail: Optional[str] = None