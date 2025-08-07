import logging
import json
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'document_id'):
            log_entry["document_id"] = record.document_id
        
        return json.dumps(log_entry)

def setup_logging():
    """Configura logging estructurado"""
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter())
    
    logger = logging.getLogger("ocr-llm")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger