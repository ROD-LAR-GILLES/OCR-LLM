# OCR-LLM

Sistema de procesamiento de documentos PDF utilizando OCR con modelos Donut y capacidades de Large Language Models.

## Descripción

OCR-LLM es una aplicación que combina técnicas de reconocimiento óptico de caracteres (OCR) con modelos de lenguaje grandes para extraer y procesar información de documentos PDF de manera inteligente. Utiliza el modelo Donut pre-entrenado para el procesamiento de documentos y Redis para optimización del rendimiento mediante caché.

## Características

- Procesamiento de documentos PDF con OCR avanzado
- Extracción de texto estructurado usando modelo Donut mejorado
- Sistema de caché con Redis para optimizar rendimiento
- API REST con FastAPI para integración
- Monitoreo con Prometheus y Grafana
- Procesamiento asíncrono y en lotes
- Arquitectura hexagonal con inyección de dependencias
- Sistema de reintentos con backoff exponencial
- Validación de calidad de OCR automática
- Soporte para GPU (opcional)
- Contenedores Docker para desarrollo y producción
- Gestión robusta de errores y excepciones

## Requisitos del Sistema

- Python 3.11+
- Docker y Docker Compose
- Redis (incluido en docker-compose)
- CUDA (opcional, para procesamiento con GPU)
- curl (para health checks)

## Instalación

### Desarrollo con Docker

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd OCR-LLM
```

2. Configurar el entorno:
```bash
make setup
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tu configuración
```

4. Iniciar el entorno de desarrollo:
```bash
make dev-up
```

5. Verificar que los servicios estén funcionando:
```bash
make health
```

### Instalación Manual

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar Redis:
```bash
redis-server
```

3. Ejecutar la aplicación:
```bash
uvicorn src.interfaces.api.main:app --reload
```

## Configuración

### Variables de Entorno

```bash
# Configuración de Donut
MODEL_NAME=naver-clova-ix/donut-base-finetuned-docvqa
USE_GPU=false
PDF_DPI=300
MAX_OUTPUT_LENGTH=2048
NUM_BEAMS=3
NUM_THREADS=4
TEMPERATURE=0.1
DOC_CONFIDENCE_THRESHOLD=0.7

# Configuración de Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL_HOURS=24
ENABLE_CACHE=true

# Paths
TEMP_DIR=/tmp/ocr-llm
INPUT_DIR=pdfs
OUTPUT_DIR=output
MODEL_CACHE_DIR=/tmp/models

# Desarrollo y Monitoreo
DEBUG=true
LOG_LEVEL=info
PROMETHEUS_ENABLED=true
JAEGER_ENDPOINT=http://localhost:14268/api/traces

# Configuraciones de Calidad y Reintentos
OCR_RETRY_ATTEMPTS=3
BATCH_SIZE=5
MAX_FILE_SIZE_MB=50
SUPPORTED_FORMATS=pdf,png,jpg,jpeg
```

## Uso

### API REST

La aplicación expone una API REST en `http://localhost:8000`

#### Procesar Documento

```bash
curl -X POST "http://localhost:8000/api/v1/documents" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@documento.pdf"
```

Respuesta esperada:
```json
{
  "document_id": "uuid-generado",
  "status": "processed",
  "pages": 3,
  "output_path": "/app/output/uuid-generado",
  "quality_score": 0.85,
  "processing_time": 12.34
}
```

#### Verificar Estado del Servicio

```bash
curl "http://localhost:8000/health"
```

#### Obtener Métricas

```bash
curl "http://localhost:8000/metrics"
```

### Usando la Librería

```python
from src.config.container import Container
from src.domain.models import ProcessDocumentRequest
from src.infrastructure.retry_service import retry_on_failure

# Configurar container
container = Container()
processor = container.document_processor()

# Procesar documento con reintentos automáticos
@retry_on_failure(max_attempts=3, base_delay=1.0)
def process_with_retry(request):
    return processor.process_document(request)

# Procesar documento
with open('documento.pdf', 'rb') as f:
    request = ProcessDocumentRequest(
        document_id="doc-001",
        content=f.read(),
        filename="documento.pdf"
    )
    
    result = process_with_retry(request)
    print(f"Procesado: {result.id}")
    print(f"Páginas: {len(result.pages)}")
    print(f"Calidad: {result.quality_metrics.confidence_score}")
```

### Procesamiento por Lotes

```python
from src.application.document_service import DocumentService

service = DocumentService(processor, max_workers=4)

# Procesar múltiples documentos
requests = [
    ProcessDocumentRequest("doc1", content1, "file1.pdf"),
    ProcessDocumentRequest("doc2", content2, "file2.pdf"),
]

results = service.process_batch(requests, batch_size=3)
```

## Arquitectura

El proyecto sigue una arquitectura hexagonal con los siguientes componentes:

```
src/
├── domain/                 # Lógica de negocio
│   ├── models.py          # Entidades del dominio
│   ├── ports.py           # Interfaces/puertos
│   ├── use_cases.py       # Casos de uso
│   └── exceptions.py      # Excepciones del dominio
├── infrastructure/        # Adaptadores de infraestructura
│   ├── donut_adapter.py       # Adaptador OCR Donut
│   ├── donut_adapter_v2.py    # Adaptador mejorado
│   ├── redis_cache.py         # Cache Redis
│   ├── file_storage.py        # Almacenamiento de archivos
│   ├── monitoring.py          # Métricas Prometheus
│   ├── logging_config.py      # Configuración de logging
│   └── retry_service.py       # Servicio de reintentos
├── application/           # Servicios de aplicación
│   ├── document_service.py    # Servicio principal
│   └── quality_service.py     # Validación de calidad
├── interfaces/            # Interfaces externas
│   └── api/              # API REST
└── config/               # Configuración
    ├── settings.py       # Configuración Pydantic
    └── container.py      # Inyección de dependencias
```

## Sistema de Calidad y Reintentos

### Validación de Calidad

El sistema incluye validación automática de la calidad del OCR:

```python
from src.application.quality_service import DocumentQualityService

quality_service = DocumentQualityService()
metrics = quality_service.assess_quality(extracted_text, confidence=0.8)

if quality_service.should_retry(metrics):
    # Reintentar procesamiento
    pass
```

### Métricas de Calidad

- **confidence_score**: Puntuación de confianza del modelo
- **text_length**: Longitud del texto extraído
- **word_count**: Número de palabras
- **special_char_ratio**: Ratio de caracteres especiales
- **readability_score**: Puntuación de legibilidad
- **has_corrupted_output**: Detección de salida corrupta

### Sistema de Reintentos

Uso del decorator para reintentos automáticos:

```python
from src.infrastructure.retry_service import retry_on_failure

@retry_on_failure(max_attempts=3, base_delay=1.0)
def process_document(document):
    # Lógica de procesamiento
    return result
```

## Monitoreo

### Prometheus
Acceder a métricas en: `http://localhost:9090`

### Grafana
Dashboard disponible en: `http://localhost:3000`
- Usuario: admin
- Contraseña: admin

### Jaeger Tracing
Trazabilidad distribuida en: `http://localhost:16686`

### Métricas Disponibles

- `ocr_documents_processed_total`: Total de documentos procesados
- `ocr_processing_seconds`: Tiempo de procesamiento
- `ocr_cache_hits_total`: Hits del caché
- `ocr_active_jobs`: Trabajos activos
- `ocr_quality_score`: Puntuación de calidad promedio
- `ocr_retry_attempts_total`: Total de reintentos

## Comandos de Desarrollo

```bash
# Configuración inicial
make setup                 # Configurar proyecto

# Gestión del entorno
make dev-up                # Iniciar entorno de desarrollo
make dev-down              # Detener servicios
make health                # Verificar estado de servicios

# Testing y calidad
make test                  # Ejecutar pruebas
make test-coverage         # Pruebas con cobertura
make quality               # Verificaciones de calidad de código

# Utilidades
make logs                  # Ver logs de la aplicación
make shell                 # Acceder al shell del contenedor
make clean                 # Limpiar sistema

# Procesamiento
make process PDF=archivo.pdf    # Procesar documento específico

# Construcción
make build                 # Construir imagen Docker
```

## Testing

### Ejecutar Pruebas

```bash
# Todas las pruebas
make test

# Pruebas específicas
pytest tests/test_integration.py -v

# Con cobertura
make test-coverage
```

### Pruebas de Calidad

```bash
# Verificar estilo de código
make quality

# Manualmente
black --check src tests
isort --check-only src tests
flake8 src tests
```

## Gestión de Errores

### Jerarquía de Excepciones

```python
OCRLLMException           # Base
├── OCRError             # Errores de OCR
├── DocumentProcessingError  # Errores de procesamiento
├── QualityError         # Errores de calidad
├── ConfigurationError   # Errores de configuración
└── RetryableError       # Errores recuperables
```

### Manejo de Errores

```python
try:
    result = processor.process_document(request)
except RetryableError as e:
    # Error recuperable, se puede reintentar
    logger.warning(f"Retryable error: {e}")
except OCRError as e:
    # Error de OCR específico
    logger.error(f"OCR failed: {e}")
except Exception as e:
    # Error inesperado
    logger.error(f"Unexpected error: {e}")
```

## Estructura de Directorios

```
OCR-LLM/
├── src/                    # Código fuente
├── tests/                  # Pruebas
├── pdfs/                   # PDFs de entrada
├── output/                 # Resultados procesados
├── logs/                   # Archivos de log
├── monitoring/             # Configuración Prometheus/Grafana
├── nginx/                  # Configuración Nginx
├── redis/                  # Configuración Redis
├── docker-compose.dev.yml  # Desarrollo
├── docker-compose.prod.yml # Producción
├── Dockerfile             # Imagen de la aplicación
├── requirements.txt       # Dependencias Python
├── Makefile              # Comandos de automatización
└── .env                  # Variables de entorno
```

## Optimización del Rendimiento

### Configuración del Modelo

Para documentos en español, usar:
```bash
MODEL_NAME=naver-clova-ix/donut-base-finetuned-docvqa
TEMPERATURE=0.1
NUM_BEAMS=3
```

### Configuración de Caché

```bash
REDIS_CACHE_TTL_HOURS=24
ENABLE_CACHE=true
```

### Procesamiento en Paralelo

```bash
NUM_THREADS=4
BATCH_SIZE=5
```

## Solución de Problemas

### Salida de OCR Corrupta

Si el OCR genera texto corrupto:

1. Verificar calidad de imagen de entrada
2. Ajustar `PDF_DPI` (recomendado: 300)
3. Usar `donut_adapter_v2.py` con mejor postprocesamiento
4. Revisar logs para patrones corruptos detectados

### Problemas de Memoria

Para documentos grandes:

1. Reducir `BATCH_SIZE`
2. Ajustar `MAX_OUTPUT_LENGTH`
3. Monitorear uso de memoria con Grafana

### Problemas de Conectividad Redis

```bash
# Verificar Redis
redis-cli ping

# Logs de Redis
docker-compose logs redis
```

## Contribución

1. Fork el proyecto
2. Crear una rama para la característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit los cambios usando Conventional Commits (`git commit -m 'feat: agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear un Pull Request

### Estándares de Código

- Seguir PEP 8 para estilo de código Python
- Usar Conventional Commits para mensajes de commit
- Incluir pruebas para nuevas características
- Documentar funciones y clases públicas
- Verificar calidad con `make quality`

### Tipos de Commit

- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `refactor`: Refactorización de código
- `test`: Agregar o modificar pruebas
- `chore`: Tareas de mantenimiento
- `perf`: Mejoras de rendimiento

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para reportar bugs o solicitar características:

1. Revisar issues existentes
2. Crear un nuevo issue con información detallada
3. Incluir logs y configuración relevante
4. Especificar pasos para reproducir el problema

## Recursos Adicionales

- [Documentación Donut](https://github.com/clovaai/donut)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Roadmap

### Versión 1.1
- Soporte para múltiples formatos de imagen
- Integración con modelos LLM adicionales
- API de webhooks para notificaciones

### Versión 1.2
- Interface web para subida de documentos
- Soporte para procesamiento distribuido
- Métricas avanzadas de calidad

### Versión 2.0
- Soporte para documentos multiidioma
- Integración con servicios cloud
