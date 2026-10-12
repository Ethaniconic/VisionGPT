from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import io
import logging

class OCRService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ocr_engine = None
        self.is_loaded = False

    def load_engine(self):
        try:
            self.logger.info("Initializing PaddleOCR...")
            self.ocr_engine = PaddleOCR(use_angle_cls=True, lang="en")
            self.is_loaded = True
            self.logger.info("PaddleOCE initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize OCR: {e}")
            raise e

    def extract_text(self, image_bytes: bytes) -> dict:
        if not self.is_loaded:
            self.load_engine()

        try:
            img = Image.open(io.BytesIO(image_bytes))
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img_np = np.array(img)
            result = self.ocr_engine.predict(img_np)
            full_text = ""
            blocks = []

            if result:
                res_list = result if isinstance(result, (list, tuple)) else [result]
                for res in res_list:
                    if not res:
                        continue
                    if isinstance(res, dict):
                        rec_texts = res.get("rec_texts", [])
                        rec_scores = res.get("rec_scores", [])
                        for text, score in zip(rec_texts, rec_scores):
                            blocks.append({"text": str(text), "confidence": float(score)})
                            full_text += str(text) + "\n"
                    elif isinstance(res, (list, tuple)):
                        for line in res:
                            if not line:
                                continue
                            if isinstance(line, (list, tuple)):
                                if len(line) >= 2 and isinstance(line[1], (list, tuple)) and len(line[1]) >= 2:
                                    text, conf = str(line[1][0]), float(line[1][1])
                                elif len(line) >= 2 and isinstance(line[0], str):
                                    text, conf = str(line[0]), float(line[1]) if isinstance(line[1], (int, float)) else 1.0
                                elif len(line) == 1:
                                    text, conf = str(line[0]), 1.0
                                else:
                                    continue
                            elif isinstance(line, str):
                                text, conf = line, 1.0
                            else:
                                continue
                            blocks.append({"text": text, "confidence": conf})
                            full_text += text + "\n"

            return {
                "success": True,
                "full_text": full_text.strip(),
                "blocks_count": len(blocks),
                "blocks": blocks
            }

        except Exception as e:
            self.logger.error(f"OCR Extraction failed: {e}")
            raise ValueError(f"OCR Processing error: {str(e)}")

ocr_service = OCRService()