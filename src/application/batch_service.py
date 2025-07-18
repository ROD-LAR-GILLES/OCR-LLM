"""
Servicio para el procesamiento por lotes de documentos.
"""
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

from domain.models import Document
from .document_service import DocumentService

@dataclass
class BatchProcessingResult:
    """
    Resultados del procesamiento por lotes.
    """
    started_at: datetime
    completed_at: Optional[datetime]
    total_documents: int
    processed_documents: int
    failed_documents: int
    documents: List[Document]

class BatchService:
    """
    Servicio para procesar lotes de documentos con seguimiento
    del progreso y manejo de errores.
    """
    
    def __init__(self, document_service: DocumentService):
        self.document_service = document_service
        
    async def process_batch(self, paths: List[str]) -> BatchProcessingResult:
        """
        Procesa un lote de documentos manteniendo estadísticas.
        
        Args:
            paths: Lista de rutas a documentos
            
        Returns:
            BatchProcessingResult: Resultado del procesamiento por lotes
        """
        started_at = datetime.now()
        processed = []
        failed = 0
        
        for path in paths:
            try:
                doc = await self.document_service.process_one(path)
                processed.append(doc)
            except Exception:
                failed += 1
                
        completed_at = datetime.now()
        
        return BatchProcessingResult(
            started_at=started_at,
            completed_at=completed_at,
            total_documents=len(paths),
            processed_documents=len(processed),
            failed_documents=failed,
            documents=processed
        )
