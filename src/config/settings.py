# src/config/container.py
from dependency_injector import containers, providers
from infrastructure.tesseract_adapter import TesseractAdapter
from infrastructure.openai_llm_adapter import OpenAIAdapter
from domain.use_cases import DocumentProcessor

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