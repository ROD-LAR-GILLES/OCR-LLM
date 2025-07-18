"""
Enrutador principal de la API REST.
"""
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from dependency_injector.wiring import inject, Provide
from ..application.document_service import DocumentService
from ..config.container import Container
from .models import (
    ProcessingOptions,
    DocumentResponse,
    BatchProcessingResponse,
    ErrorResponse
)

router = APIRouter(prefix="/api/v1")

@router.post(
    "/documents",
    response_model=DocumentResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    tags=["documents"]
)
@inject
async def process_document(
    file: UploadFile = File(...),
    options: ProcessingOptions = Depends(),
    document_service: DocumentService = Depends(Provide[Container.document_service])
):
    """
    Procesa un único documento.
    
    Args:
        file: Archivo a procesar
        options: Opciones de procesamiento
        document_service: Servicio de procesamiento inyectado
        
    Returns:
        DocumentResponse: Información del documento procesado
    """
    try:
        # Guardar archivo temporalmente
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Procesar documento
        document = await document_service.process_one(
            temp_path,
            options=options
        )
        
        return DocumentResponse(
            id=document.id,
            original_name=file.filename,
            text=document.text,
            processed_at=document.processed_at,
            processing_time=document.processing_time,
            quality_score=document.quality_score,
            page_count=len(document.pages),
            word_count=len(document.text.split())
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post(
    "/documents/batch",
    response_model=BatchProcessingResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    tags=["documents"]
)
@inject
async def process_batch(
    files: List[UploadFile] = File(...),
    options: ProcessingOptions = Depends(),
    document_service: DocumentService = Depends(Provide[Container.document_service])
):
    """
    Procesa múltiples documentos en lote.
    
    Args:
        files: Lista de archivos a procesar
        options: Opciones de procesamiento
        document_service: Servicio de procesamiento inyectado
        
    Returns:
        BatchProcessingResponse: Información del procesamiento por lotes
    """
    try:
        # Guardar archivos temporalmente
        paths = []
        for file in files:
            temp_path = f"/tmp/{file.filename}"
            with open(temp_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            paths.append(temp_path)
        
        # Procesar documentos
        batch_result = await document_service.process_batch(
            paths,
            options=options
        )
        
        return BatchProcessingResponse(
            batch_id=batch_result.id,
            total_documents=len(files),
            processed_documents=len(batch_result.documents),
            failed_documents=batch_result.failed_documents,
            started_at=batch_result.started_at,
            completed_at=batch_result.completed_at,
            documents=[
                DocumentResponse(
                    id=doc.id,
                    original_name=doc.original_name,
                    text=doc.text,
                    processed_at=doc.processed_at,
                    processing_time=doc.processing_time,
                    quality_score=doc.quality_score,
                    page_count=len(doc.pages),
                    word_count=len(doc.text.split())
                )
                for doc in batch_result.documents
            ]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
