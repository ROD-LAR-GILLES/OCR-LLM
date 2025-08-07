import pytest
from config.container import Container
from domain.models import ProcessDocumentRequest
import os

@pytest.fixture
def container():
    """Container configurado para testing"""
    container = Container()
    container.config.from_dict({
        "donut": {
            "model_name": "test-model",
            "use_gpu": False
        }
    })
    return container

@pytest.mark.integration
def test_end_to_end_processing(container, sample_pdf):
    """Test completo del flujo de procesamiento"""
    processor = container.document_processor()
    
    request = ProcessDocumentRequest(
        document_id="test-123",
        content=sample_pdf,
        filename="test.pdf"
    )
    
    result = processor.process_document(request)
    
    assert result.id == "test-123"
    assert len(result.pages) > 0
    assert result.output_path is not None
    assert os.path.exists(result.output_path)