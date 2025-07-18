# src/config/container.py
from dependency_injector import containers, providers
from infrastructure.tesseract_adapter import TesseractAdapter
from infrastructure.openai_llm_adapter import OpenAIAdapter
from domain.use_cases import DocumentProcessor
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Donut Configuration
    model_name: str = "naver-clova-ix/donut-base-finetuned-cord-v2"
    use_gpu: bool = False
    pdf_dpi: int = 200
    max_output_length: int = 1024
    num_beams: int = 4
    num_threads: int = 4
    temperature: float = 0.8
    
    # Paths
    temp_dir: str = "/tmp/ocr-llm"
    input_dir: str = "pdfs"
    output_dir: str = "output"

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    ocr_service = providers.Singleton(
        TesseractAdapter,
        config=config.ocr
    )
    
    llm_service = providers.Singleton(
        OpenAIAdapter,
        api_key=config.openai.api_key,
        model=config.openai.model
    )
    
    storage_service = providers.Singleton(
        FileStorageAdapter,
        base_path=config.storage.path
    )
    
    document_processor = providers.Singleton(
        DocumentProcessor,
        ocr_service=ocr_service,
        llm_service=llm_service,
        storage_service=storage_service
    )