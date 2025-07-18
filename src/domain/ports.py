from abc import ABC, abstractmethod
from .models import Document, Page

class OcrPort(ABC):
    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        """Extrae texto de una imagen usando OCR"""
        pass

class StoragePort(ABC):
    @abstractmethod
    def save_document(self, document: Document) -> str:
        """Guarda un documento procesado"""
        pass

    @abstractmethod
    def load_document(self, path: str) -> Document:
        """Carga un documento procesado"""
        pass
