from dependency_injector import containers, providers
from infrastructure.donut_adapter import DonutAdapter
from infrastructure.file_storage import LocalFileStorage
from domain.use_cases import DocumentProcessor

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    ocr_service = providers.Singleton(
        DonutAdapter,
        settings=config
    )
    
    storage_service = providers.Singleton(
        LocalFileStorage,
        base_path=config.output_dir
    )
    
    document_processor = providers.Singleton(
        DocumentProcessor,
        ocr_service=ocr_service,
        storage_service=storage_service
    )