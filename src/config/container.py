from dependency_injector import containers, providers
from .settings import Settings
from infrastructure.redis_cache import RedisCache
from infrastructure.donut_adapter import DonutAdapter
from infrastructure.file_storage import LocalFileStorage
from domain.use_cases import DocumentProcessor

class Container(containers.DeclarativeContainer):
    """Contenedor de dependencias para la aplicación."""
    
    config = providers.Singleton(Settings)
    
    # Servicios base
    cache = providers.Singleton(
        RedisCache,
        redis_url=config.provided.redis_url
    ) if config.provided.enable_cache else None
    
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