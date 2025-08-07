from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from config.container import Container
from domain.models import ProcessDocumentRequest, Document
import uuid

app = FastAPI(
    title="OCR-LLM API",
    description="API para procesamiento de documentos con OCR y LLM",
    version="1.0.0"
)

container = Container()

@app.post("/api/v1/documents", response_model=dict)
async def process_document(file: UploadFile = File(...)):
    """Procesa un documento PDF"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Solo se admiten archivos PDF")
    
    try:
        content = await file.read()
        request = ProcessDocumentRequest(
            document_id=str(uuid.uuid4()),
            content=content,
            filename=file.filename
        )
        
        processor = container.document_processor()
        result = processor.process_document(request)
        
        return {
            "document_id": result.id,
            "status": "processed",
            "pages": len(result.pages),
            "output_path": result.output_path
        }
    except Exception as e:
        raise HTTPException(500, f"Error procesando documento: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {"status": "healthy", "service": "ocr-llm"}

@app.get("/metrics")
async def metrics():
    """Métricas del servicio"""
    return {"processed_documents": 0, "cache_hits": 0}