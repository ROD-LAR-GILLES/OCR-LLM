# OCR-LLM

Sistema de procesamiento de documentos PDF utilizando OCR con modelos Donut y capacidades de Large Language Models.

## Descripción

OCR-LLM es una aplicación que combina técnicas de reconocimiento óptico de caracteres (OCR) con modelos de lenguaje grandes para extraer y procesar información de documentos PDF de manera inteligente. Utiliza el modelo Donut pre-entrenado para el procesamiento de documentos y Redis para optimización del rendimiento mediante caché.

## Características

- Procesamiento de documentos PDF con OCR avanzado
- Extracción de texto estructurado usando modelo Donut
- Sistema de caché con Redis para optimizar rendimiento
- API REST con FastAPI para integración
- Monitoreo con Prometheus y Grafana
- Procesamiento asíncrono y en lotes
- Arquitectura hexagonal con inyección de dependencias
- Soporte para GPU (opcional)
- Contenedores Docker para desarrollo y producción

## Requisitos del Sistema

- Python 3.11+
- Docker y Docker Compose
- Redis (incluido en docker-compose)
- CUDA (opcional, para procesamiento con GPU)

## Instalación

### Desarrollo con Docker

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd OCR-LLM
```

2. Construir y ejecutar los contenedores:
```bash
docker-compose up --build
```

3. Acceder a la API:
```
http://localhost:8000/api/docs
```

### Desarrollo Local

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd OCR-LLM
```

2. Crear un entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. Ejecutar la aplicación:
```bash
uvicorn src.main:app --reload
```

## Uso

### Procesamiento de Documentos

- **Procesar un documento**:
```python
from app.services.document_service import DocumentService

document_service = DocumentService()
document = document_service.process_one("ruta/al/documento.pdf")
print(document.text)
```

- **Procesar múltiples documentos**:
```python
documents = document_service.process_batch(["ruta/al/doc1.pdf", "ruta/al/doc2.pdf"])
```

### API REST

- **Iniciar la API**:
```bash
uvicorn src.interfaces.api.app:app --reload
```

- **Ejemplo de solicitud para procesar un documento**:
```bash
curl -X POST http://localhost:8000/api/v1/documents \
  -F "file=@ruta/al/documento.pdf" \
  -F "quality=90"
```

## Monitoreo

El proyecto incluye endpoints de monitoreo:

- `/metrics` - Métricas Prometheus
- `/health` - Estado del servicio
- `/docs` - Documentación OpenAPI

## Documentación

- [Guía de Instalación](docs/installation.md)
- [Documentación de la API](docs/api.md)
- [Guía de Desarrollo](docs/development.md)
- [Arquitectura](docs/architecture.md)

## Desarrollo

### Configuración del Entorno

```bash
# Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar pruebas
pytest

# Verificar formato
black src tests
isort src tests

# Verificar tipos
mypy src tests
```

### Docker

```bash
# Construir imagen
docker build -t ocr-llm .

# Ejecutar
docker run -p 8000:8000 ocr-llm
```

## Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee nuestra [Guía de Contribución](CONTRIBUTING.md).

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Agradecimientos

- OpenAI por la API GPT
- Tesseract OCR
- La comunidad de código abierto

---

No olvides dar una estrella si encuentras útil este proyecto!
