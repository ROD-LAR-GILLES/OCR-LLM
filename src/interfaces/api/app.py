"""
Aplicación principal FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from .router import router
from ..config.container import Container

def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    
    Returns:
        FastAPI: Aplicación configurada
    """
    # Crear contenedor de dependencias
    container = Container()
    
    # Crear aplicación
    app = FastAPI(
        title="OCR-LLM API",
        description="API REST para procesamiento de documentos con OCR",
        version="1.0.0"
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Montar métricas Prometheus
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    
    # Incluir rutas
    app.include_router(router)
    
    # Configurar inyección de dependencias
    container.wire(modules=[".router"])
    
    return app

app = create_app()
