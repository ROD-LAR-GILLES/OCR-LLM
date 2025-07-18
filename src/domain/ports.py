from abc import ABC, abstractmethod
from .models import Document, Page

class OcrPort(ABC):
    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        """Extrae texto de una imagen usando OCR"""
        pass

class PdfPort(ABC):
    @abstractmethod
    def extract_pages(self, pdf_path: str) -> list[bytes]:
        """Extrae las páginas de un PDF como imágenes"""
        pass
            
    @abstractmethod
    def save_with_text(self, pdf_path: str, document: Document) -> str:
        """Guarda un PDF con el texto refinado incrustado"""
        pass

class LlmPort(ABC):
    @abstractmethod
    def refine(self, text: str) -> str:
        """Refina el texto usando un modelo de lenguaje"""
        pass

    @abstractmethod
    def batch_refine(self, texts: list[str]) -> list[str]:
        """Refina múltiples textos en batch"""
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
