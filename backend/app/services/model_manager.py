import torch
from transformers import BlipProcessor, BlipForQuestionAnswering
import logging

class ModelManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = None
        self.model = None
        self.is_loaded = False

    def load_models(self):
        try:
            logging.info(f"Loading models on device: {self.device}")
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
            self.model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
            self.model = self.model.to(self.device)

            self.model.eval()
            self.is_loaded = True

            logging.info("Models loaded successfully")
        
        except Exception as e:
            logging.error(f"Failed to load the models: {e}")
            raise e

    def get_model_info(self):
        return {
            "device": str(self.device),
            "loaded": self.is_loaded,
            "model_name": "blip-vqa-base"
        }

model_manager = ModelManager()