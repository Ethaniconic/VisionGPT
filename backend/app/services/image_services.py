import io
from PIL import Image, ImageOps
import logging

MAX_FILE_SIZE_MB = 10
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAGIC_NUMBERS = {
    b'\xff\xd8\xff': 'JPEG',
    b'\x89PNG\r\n\x1a\n': 'PNG',
    b'RIFF': 'WEBP',
}

def validate_and_process_image(file_content: bytes, mime_type: str) -> dict:
    if len(file_content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError("File size exceeds the max limit.")

    img = io.BytesIO(file_content)
    first_bytes = file_content[:8]

    detected_format = None        
    for magic, file_type in MAGIC_NUMBERS.items():
        if first_bytes.startswith(magic):
            detected_format = file_type
            break
    
    if not detected_format:
        try:
            detected_format = Image.open(io.BytesIO(file_content)).format
        except Exception:
            raise ValueError("Invalid file format.")

    try:
        verify_img = Image.open(io.BytesIO(file_content))
        verify_img.verify()
        logging.info("File verified successfully.")
    except Exception as e:
        raise ValueError(f"Corrupted image file: {e}")
    
    img = Image.open(io.BytesIO(file_content))

    img_format = img.format or detected_format
    exif_img = ImageOps.exif_transpose(img)
    rgb_img = exif_img.convert("RGB")

    width, height = rgb_img.size

    return {
        "success": True,
        "message": "Image processed successfully",
        "width": width,
        "height": height,
        "format": img_format,
        "img_format": img_format,
        "img_object": rgb_img
    }