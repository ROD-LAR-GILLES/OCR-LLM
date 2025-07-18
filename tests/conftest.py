"""
Fixtures compartidos para pruebas.
"""
import os
from pathlib import Path
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from domain.models import Document, Page
from domain.ports import OcrPort, StoragePort
from infrastructure.donut_adapter import DonutAdapter
from infrastructure.file_storage import LocalFileStorage
from infrastructure.monitoring import DocumentProcessingTracer
from application.document_service import DocumentService
from interfaces.api.app import create_app

# Inicializar Faker para datos de prueba
fake = Faker()

@pytest.fixture
def test_dir(tmp_path):
    """Directorio temporal para pruebas."""
    return tmp_path

@pytest.fixture
def mock_ocr():
    """Mock del servicio OCR."""
    class MockOCR(OcrPort):
        def extract_text(self, image_path: str) -> str:
            return fake.text()
    return MockOCR()

@pytest.fixture
def mock_storage(test_dir):
    """Mock del servicio de almacenamiento."""
    class MockStorage(StoragePort):
        def save_document(self, document: Document) -> str:
            path = test_dir / f"{document.id}.json"
            return str(path)
            
        def load_document(self, path: str) -> Document:
            return Document(
                id=fake.uuid4(),
                pages=[
                    Page(
                        number=1,
                        text=fake.text()
                    )
                ]
            )
    return MockStorage()

@pytest.fixture
def document_service(mock_ocr, mock_storage):
    """Servicio de documentos con dependencias mockeadas."""
    return DocumentService(
        ocr=mock_ocr,
        storage=mock_storage
    )

@pytest.fixture
def test_app(document_service):
    """Aplicación FastAPI para pruebas."""
    app = create_app()
    app.dependency_overrides[DocumentService] = lambda: document_service
    return app

@pytest.fixture
def test_client(test_app):
    """Cliente HTTP para pruebas de la API."""
    return TestClient(test_app)

@pytest.fixture
def sample_pdf(test_dir):
    """Crea un PDF de prueba."""
    pdf_path = test_dir / "test.pdf"
    # Crear un PDF básico para pruebas
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.7\n%\x80\x80\x80\x80\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n>>\n/MediaBox [0 0 595 842]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000015 00000 n\n0000000061 00000 n\n0000000114 00000 n\ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n178\n%%EOF\n")
    return pdf_path

@pytest.fixture
def sample_document():
    """Crea un documento de prueba."""
    return Document(
        id=fake.uuid4(),
        pages=[
            Page(
                number=1,
                text=fake.text()
            ),
            Page(
                number=2,
                text=fake.text()
            )
        ]
    )
