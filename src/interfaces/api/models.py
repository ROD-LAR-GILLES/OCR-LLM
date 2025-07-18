"""
Modelos de datos para la API REST.
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ProcessingOptions(BaseModel):
    """Opciones para el procesamiento de documentos"""
    quality: int = Field(
        default=90,
        ge=1,
        le=100,
        description="Calidad del procesamiento OCR (1-100)"
    )
    language: str = Field(
        default="es",
        description="Idioma principal del documento"
    )
    format: str = Field(
        default="text",
        description="Formato de salida deseado (text, markdown, json)"
    )

class DocumentResponse(BaseModel):
    """Respuesta con información del documento procesado"""
    id: str
    original_name: str
    text: str
    processed_at: datetime
    processing_time: float
    quality_score: Optional[float] = None
    page_count: int
    word_count: int

class BatchProcessingResponse(BaseModel):
    """Respuesta para el procesamiento por lotes"""
    batch_id: str
    total_documents: int
    processed_documents: int
    failed_documents: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    documents: List[DocumentResponse]

class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    detail: str
    error_code: str
    timestamp: datetime = Field(default_factory=datetime.now)
    path: Optional[str] = None
