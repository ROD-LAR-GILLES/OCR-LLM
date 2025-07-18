"""
Servicio de aplicación para el procesamiento de documentos.
"""
from typing import List
import asyncio
from datetime import datetime

from domain.models import Document
from domain.ports import OcrPort, StoragePort

class DocumentService:
    """
    Servicio principal para el procesamiento de documentos.
    Coordina las operaciones entre el OCR y el almacenamiento.
    """
    
    def __init__(self, ocr: OcrPort, storage: StoragePort):
        self.ocr = ocr
        self.storage = storage
        
    async def process_one(self, path: str) -> Document:
        """
        Procesa un único documento.
        
        Args:
            path: Ruta al documento a procesar
            
        Returns:
            Document: Documento procesado con su texto extraído
        """
        # Extraer texto usando OCR
        text = await self.ocr.extract_text(path)
        
        # Crear documento
        document = Document(
            path=path,
            text=text,
            processed_at=datetime.now()
        )
        
        # Guardar documento
        saved_path = await self.storage.save_document(document)
        document.storage_path = saved_path
        
        return document
        
    async def process_batch(self, paths: List[str]) -> List[Document]:
        """
        Procesa múltiples documentos en paralelo.
        
        Args:
            paths: Lista de rutas a documentos
            
        Returns:
            List[Document]: Lista de documentos procesados
        """
        tasks = [self.process_one(path) for path in paths]
        return await asyncio.gather(*tasks)
