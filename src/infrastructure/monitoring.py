"""
Módulo de monitoreo y observabilidad para el procesamiento de documentos.
"""
from typing import Any, Dict, Optional
import structlog
from opentelemetry import trace
from opentelemetry.trace import Span, Status, StatusCode
from prometheus_client import Counter, Histogram, Info

# Configuración de logging estructurado
logger = structlog.get_logger(__name__)

# Métricas Prometheus
DOCUMENTS_PROCESSED = Counter(
    "documents_processed_total",
    "Total number of documents processed",
    ["status"]
)

PROCESSING_TIME = Histogram(
    "document_processing_seconds",
    "Time spent processing documents",
    ["operation"]
)

OCR_QUALITY = Histogram(
    "ocr_quality_score",
    "Quality score of OCR results",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

MODEL_INFO = Info(
    "model_information",
    "Information about the OCR model being used"
)

class DocumentProcessingTracer:
    """
    Clase para rastrear el procesamiento de documentos usando OpenTelemetry.
    """
    
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
    
    def start_processing(self, document_id: str) -> Span:
        """
        Inicia el rastreo del procesamiento de un documento.
        
        Args:
            document_id: Identificador único del documento
            
        Returns:
            Span: El span de rastreo iniciado
        """
        return self.tracer.start_as_current_span(
            "process_document",
            attributes={"document.id": document_id}
        )
    
    def record_success(self, span: Span, metadata: Dict[str, Any]):
        """
        Registra el éxito del procesamiento.
        
        Args:
            span: Span actual de rastreo
            metadata: Metadatos del procesamiento
        """
        span.set_status(Status(StatusCode.OK))
        span.set_attributes(metadata)
        DOCUMENTS_PROCESSED.labels(status="success").inc()
        
    def record_error(self, span: Span, error: Exception):
        """
        Registra un error en el procesamiento.
        
        Args:
            span: Span actual de rastreo
            error: Excepción ocurrida
        """
        span.set_status(Status(StatusCode.ERROR))
        span.record_exception(error)
        DOCUMENTS_PROCESSED.labels(status="error").inc()
        logger.error("document_processing_error", error=str(error))

class MetricsCollector:
    """
    Colector de métricas para el monitoreo del sistema.
    """
    
    @staticmethod
    def record_processing_time(operation: str, duration: float):
        """
        Registra el tiempo de procesamiento de una operación.
        
        Args:
            operation: Nombre de la operación
            duration: Duración en segundos
        """
        PROCESSING_TIME.labels(operation=operation).observe(duration)
    
    @staticmethod
    def record_ocr_quality(score: float):
        """
        Registra la calidad del OCR.
        
        Args:
            score: Puntuación de calidad (0-1)
        """
        OCR_QUALITY.observe(score)
    
    @staticmethod
    def update_model_info(model_name: str, version: str):
        """
        Actualiza la información del modelo.
        
        Args:
            model_name: Nombre del modelo
            version: Versión del modelo
        """
        MODEL_INFO.info({
            "name": model_name,
            "version": version
        })
