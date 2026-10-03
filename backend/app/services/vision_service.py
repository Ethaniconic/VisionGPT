import torch
from PIL import Image
import io
from app.services.model_manager import model_manager

class VisionService:
    def __init__(self):
        self.processor = model_manager.processor
        self.model = model_manager.model
        self.device = model_manager.device

    async def ask_question(self, image_bytes: bytes, question: str) -> str:
        try:
            processor = model_manager.processor
            model = model_manager.model
            device = model_manager.device

            if processor is None or model is None:
                raise ValueError("Model is not loaded yet.")

            img = Image.open(io.BytesIO(image_bytes))
            rgb_img = img.convert("RGB")
            inputs = processor(images=rgb_img, text=question, return_tensors="pt")
            inputs = {
                k: v.to(device) for k, v in inputs.items()
            }

            with torch.no_grad():
                generated_ids = model.generate(**inputs, max_new_tokens=100)

            answer = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

            del inputs, generated_ids

            return answer.strip()

        except Exception as e:
            raise ValueError(f"Inference failed: {str(e)}")

vision_service = VisionService()