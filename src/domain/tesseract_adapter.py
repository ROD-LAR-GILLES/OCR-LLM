#tesseract_adapter.py
import pytesseract
from domain.ports import OcrPort

class TesseractAdapter(OcrPort):
    def __init__(self, config: dict = None):
        self.config = config or {}
        
    def extract_text(self, image_path: str) -> str:
        return pytesseract.image_to_string(
            image_path,
            lang=self.config.get('lang', 'spa'),
            config=self.config.get('tesseract_config', '')
        )
