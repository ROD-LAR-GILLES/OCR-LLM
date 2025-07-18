"""
Value Objects para el dominio de procesamiento de documentos.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

@dataclass(frozen=True)
class ProcessingMetadata:
    """
    Value object inmutable para mantener la metadata del procesamiento
    de documentos.
    
    Attributes:
        started_at: Momento de inicio del procesamiento
        completed_at: Momento de finalización del procesamiento
        processor_version: Versión del procesador usado
        processing_stats: Estadísticas del procesamiento
    """
    started_at: datetime
    completed_at: datetime
    processor_version: str
    processing_stats: Dict[str, Any]
    
@dataclass(frozen=True)
class DocumentIdentifier:
    """
    Value object inmutable para identificar documentos de manera única.
    
    Attributes:
        id: Identificador único del documento
        version: Versión del documento
    """
    id: str
    version: int = 1
    
@dataclass(frozen=True)
class ProcessingOptions:
    """
    Value object inmutable para configurar el procesamiento de documentos.
    
    Attributes:
        quality: Nivel de calidad del OCR (1-100)
        format: Formato de salida deseado
        language: Idioma principal del documento
    """
    quality: int = 90
    format: str = "text"
    language: str = "es"
