"""
Servicio de aplicación para el procesamiento de documentos.
"""
from typing import List, Optional
import asyncio
import hashlib
from datetime import datetime, timedelta

from domain.models import Document
from domain.ports import OcrPort, StoragePort
from domain.cache_port import CachePort

class DocumentService:
    """
    Servicio principal para el procesamiento de documentos.
    Coordina las operaciones entre el OCR y el almacenamiento.
    """
    
    def __init__(self, ocr: OcrPort, storage: StoragePort, cache: Optional[CachePort] = None):
        self.ocr = ocr
        self.storage = storage
        self.cache = cache
        self.cache_ttl = timedelta(hours=24)  # Cache por 24 horas por defecto
        
    def _generate_cache_key(self, path: str) -> str:
        """Genera una clave única para el caché basada en el path y el contenido del archivo"""
        return f"ocr:document:{hashlib.sha256(path.encode()).hexdigest()}"
        
    async def process_one(self, path: str) -> Document:
        """
        Procesa un único documento.
        
        Args:
            path: Ruta al documento a procesar
            
        Returns:
            Document: Documento procesado con su texto extraído
        """
        # Verificar caché si está disponible
        if self.cache:
            cache_key = self._generate_cache_key(path)
            cached_doc = await self.cache.get(cache_key)
            if cached_doc:
                return Document(**cached_doc)
        
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
        
        # Guardar en caché si está disponible
        if self.cache:
            cache_key = self._generate_cache_key(path)
            await self.cache.set(
                cache_key, 
                document.dict(), 
                ttl=self.cache_ttl
            )
        
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
