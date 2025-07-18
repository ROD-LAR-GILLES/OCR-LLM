"""
Pruebas de integración para la API REST.
"""
import pytest
from fastapi import status

def test_process_single_document(test_client, sample_pdf):
    """Prueba el endpoint de procesamiento de un documento."""
    # Given
    with open(sample_pdf, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        data = {"quality": 90, "language": "es"}
        
        # When
        response = test_client.post("/api/v1/documents", files=files, data=data)
        
        # Then
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert "id" in result
        assert "text" in result
        assert "processed_at" in result
        assert result["original_name"] == "test.pdf"

def test_process_batch_documents(test_client, test_dir):
    """Prueba el endpoint de procesamiento por lotes."""
    # Given
    files = []
    for i in range(3):
        pdf_path = test_dir / f"test_{i}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.7\n")
        files.append(("files", (f"test_{i}.pdf", open(pdf_path, "rb"), "application/pdf")))
    
    # When
    response = test_client.post("/api/v1/documents/batch", files=files)
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total_documents"] == 3
    assert result["processed_documents"] == 3
    assert len(result["documents"]) == 3

def test_invalid_file_type(test_client, test_dir):
    """Prueba el manejo de tipos de archivo inválidos."""
    # Given
    txt_path = test_dir / "test.txt"
    with open(txt_path, "w") as f:
        f.write("This is not a PDF")
    
    with open(txt_path, "rb") as f:
        files = {"file": ("test.txt", f, "text/plain")}
        
        # When
        response = test_client.post("/api/v1/documents", files=files)
        
        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error_code" in response.json()

def test_metrics_endpoint(test_client):
    """Prueba el endpoint de métricas."""
    # When
    response = test_client.get("/metrics")
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert "application/openmetrics-text" in response.headers["content-type"]
    
def test_cors_headers(test_client):
    """Prueba la configuración de CORS."""
    # When
    response = test_client.options("/api/v1/documents")
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"
