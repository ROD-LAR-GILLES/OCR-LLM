"""
Servicio de aplicación para el procesamiento de documentos.
"""
from typing import List, Optional
import asyncio
import hashlib
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

from domain.models import Document, ProcessDocumentRequest
from domain.ports import OcrPort, StoragePort
from domain.cache_port import CachePort

class DocumentService:
    """
    Servicio principal para el procesamiento de documentos.
    Coordina las operaciones entre el OCR y el almacenamiento.
    """
    
    def __init__(self, ocr: OcrPort, storage: StoragePort, cache: Optional[CachePort] = None, max_workers: int = 4):
        self.ocr = ocr
        self.storage = storage
        self.cache = cache
        self.cache_ttl = timedelta(hours=24)  # Cache por 24 horas por defecto
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
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
        
    async def process_documents_async(
        self, 
        requests: List[ProcessDocumentRequest]
    ) -> List[Document]:
        """Procesa múltiples documentos de forma asíncrona"""
        loop = asyncio.get_event_loop()
        
        tasks = [
            loop.run_in_executor(
                self.executor, 
                self.ocr.extract_text, 
                request
            )
            for request in requests
        ]
        
        return await asyncio.gather(*tasks)
    
    def process_batch(
        self, 
        requests: List[ProcessDocumentRequest],
        batch_size: int = 3
    ) -> List[Document]:
        """Procesa en lotes para optimizar memoria"""
        results = []
        for i in range(0, len(requests), batch_size):
            batch = requests[i:i + batch_size]
            batch_results = asyncio.run(self.process_documents_async(batch))
            results.extend(batch_results)
        return results
