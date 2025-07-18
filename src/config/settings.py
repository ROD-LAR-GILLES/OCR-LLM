"""
Configuración principal del proyecto OCR-LLM usando Donut.
"""

from dependency_injector import containers, providers
from infrastructure.donut_adapter import DonutAdapter
from infrastructure.file_storage import LocalFileStorage
from domain.use_cases import DocumentProcessor
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """
    Configuración para el procesamiento de documentos con Donut.
    
    Attributes:
        model_name: Nombre del modelo pre-entrenado de Donut
        use_gpu: Si se debe usar GPU para el procesamiento
        pdf_dpi: Resolución para la conversión de PDF a imagen
        max_output_length: Longitud máxima del texto generado
        num_beams: Número de beams para la búsqueda
        num_threads: Hilos para procesamiento paralelo
        temperature: Temperatura para la generación de texto
        redis_url: URL de conexión a Redis
        redis_cache_ttl_hours: Tiempo de vida del caché en horas
        enable_cache: Si se debe utilizar el caché
    """
    # Configuración de Donut
    model_name: str = "naver-clova-ix/donut-base-finetuned-cord-v2"
    use_gpu: bool = False
    pdf_dpi: int = 200
    max_output_length: int = 1024
    num_beams: int = 4
    num_threads: int = 4
    temperature: float = 0.8
    
    # Configuración de Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_ttl_hours: int = 24
    enable_cache: bool = True
    
    # Paths
    temp_dir: Path = Path("/tmp/ocr-llm")
    input_dir: Path = Path("pdfs")
    output_dir: Path = Path("output")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

# La clase Container se ha movido a container.py