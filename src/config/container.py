from dependency_injector import containers, providers
from infrastructure.donut_adapter import DonutAdapter
from infrastructure.file_storage import LocalFileStorage
from infrastructure.redis_cache import RedisCache
from domain.use_cases import DocumentProcessor
from config.settings import Settings

class Container(containers.DeclarativeContainer):
    # Configuración
    config = providers.Configuration()
    settings = providers.Singleton(Settings)
    
    # Servicios de infraestructura
    donut_adapter = providers.Singleton(
        DonutAdapter,
        config=config.donut
    )
    
    file_storage = providers.Singleton(
        LocalFileStorage,
        base_path=settings.provided.output_dir
    )
    
    redis_cache = providers.Singleton(
        RedisCache,
        redis_url=settings.provided.redis_url,
        ttl_hours=settings.provided.redis_cache_ttl_hours
    )
    
    # Casos de uso
    document_processor = providers.Singleton(
        DocumentProcessor,
        ocr=donut_adapter,
        storage=file_storage,
        cache=redis_cache
    )