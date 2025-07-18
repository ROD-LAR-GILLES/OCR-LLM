"""
Pruebas unitarias para el servicio de documentos.
"""
import pytest
from pathlib import Path
from domain.models import Document

pytestmark = pytest.mark.asyncio

async def test_process_one_document(document_service, sample_pdf):
    """Prueba el procesamiento de un documento individual."""
    # When
    document = await document_service.process_one(str(sample_pdf))
    
    # Then
    assert document is not None
    assert isinstance(document, Document)
    assert document.id is not None
    assert len(document.pages) > 0
    assert document.pages[0].text is not None

async def test_process_batch_documents(document_service, test_dir):
    """Prueba el procesamiento por lotes de documentos."""
    # Given
    paths = []
    for i in range(3):
        pdf_path = test_dir / f"test_{i}.pdf"
        # Crear PDFs de prueba
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.7\n")
        paths.append(str(pdf_path))
    
    # When
    results = await document_service.process_batch(paths)
    
    # Then
    assert results is not None
    assert len(results) == 3
    for doc in results:
        assert isinstance(doc, Document)
        assert doc.id is not None
        assert len(doc.pages) > 0

async def test_process_one_document_with_error(document_service, test_dir):
    """Prueba el manejo de errores al procesar un documento."""
    # Given
    non_existent_path = test_dir / "non_existent.pdf"
    
    # When/Then
    with pytest.raises(FileNotFoundError):
        await document_service.process_one(str(non_existent_path))

async def test_document_caching(document_service, sample_pdf, mock_ocr, mocker):
    """Prueba que el caché funciona correctamente."""
    # Given
    spy = mocker.spy(mock_ocr, "extract_text")
    
    # When
    doc1 = await document_service.process_one(str(sample_pdf))
    doc2 = await document_service.process_one(str(sample_pdf))
    
    # Then
    assert doc1.id == doc2.id
    assert spy.call_count == 1  # El OCR solo se llamó una vez

async def test_process_one_with_options(document_service, sample_pdf):
    """Prueba el procesamiento con opciones personalizadas."""
    # Given
    options = {
        "quality": 100,
        "language": "es"
    }
    
    # When
    document = await document_service.process_one(
        str(sample_pdf),
        options=options
    )
    
    # Then
    assert document is not None
    assert document.processing_options == options
