from typing import Optional, Dict, Any

class OCRLLMException(Exception):
    """Excepción base para el sistema OCR-LLM"""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}

class OCRError(OCRLLMException):
    """Error en el procesamiento OCR"""
    pass

class DocumentProcessingError(OCRLLMException):
    """Error en el procesamiento de documentos"""
    pass

class QualityError(OCRLLMException):
    """Error de calidad en el resultado"""
    pass

class ConfigurationError(OCRLLMException):
    """Error de configuración"""
    pass

class RetryableError(OCRLLMException):
    """Error que puede ser reintentado"""
    def __init__(self, message: str, max_retries: int = 3, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.max_retries = max_retries