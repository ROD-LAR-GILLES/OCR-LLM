# OCR-LLM

Sistema de OCR basado en el modelo Donut con procesamiento asíncrono y API REST.

[![CI/CD](https://github.com/ROD-LAR-GILLES/OCR-LLM/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/ROD-LAR-GILLES/OCR-LLM/actions/workflows/ci-cd.yml)
[![Coverage](https://codecov.io/gh/ROD-LAR-GILLES/OCR-LLM/branch/main/graph/badge.svg)](https://codecov.io/gh/ROD-LAR-GILLES/OCR-LLM)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Características

- 🔍 OCR de alta precisión usando el modelo Donut
- 🚀 Procesamiento asíncrono de documentos
- 📊 API REST con FastAPI
- 💾 Sistema de caché con Redis
- 📈 Monitoreo y métricas con Prometheus
- 🔄 Soporte para procesamiento por lotes

## Inicio Rápido

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/ROD-LAR-GILLES/OCR-LLM.git
cd OCR-LLM

# Crear un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -e ".[dev]"
```

### Uso Básico

```python
from ocr_llm.application.document_service import DocumentService

# Procesar un documento
document = await document_service.process_one("documento.pdf")
print(document.text)

# Procesar múltiples documentos
documents = await document_service.process_batch(["doc1.pdf", "doc2.pdf"])
```

### Uso de la API

```bash
# Iniciar la API
uvicorn src.interfaces.api.app:app --reload

# Procesar un documento vía API
curl -X POST http://localhost:8000/api/v1/documents \
  -F "file=@documento.pdf" \
  -F "quality=90"
```

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

## Monitoreo

El proyecto incluye endpoints de monitoreo:

- `/metrics` - Métricas Prometheus
- `/health` - Estado del servicio
- `/docs` - Documentación OpenAPI

## Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee nuestra [Guía de Contribución](CONTRIBUTING.md).

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.: Procesamiento de Documentos con OCR y LLM

Sistema de procesamiento de documentos PDF que combina OCR avanzado usando Donut (Document Understanding Transformer) con LLM (Modelos de Lenguaje Grande) para extraer y mejorar texto de documentos escaneados.

## 🚀 Características

- **OCR Avanzado con Donut**: Extracción de texto estructurado sin dependencia de Tesseract
- **Reconocimiento de Estructura**: Detecta párrafos, tablas y encabezados
- **Procesamiento en Lotes**: Maneja múltiples documentos eficientemente
- **Mejora con LLM**: Refina y estructura el texto extraído
- **Flexible**: Soporta múltiples motores OCR (Donut, Tesseract, DocTR)

## 🛠️ Motores OCR Disponibles

1. **Donut** (Predeterminado)
   - Basado en transformers
   - Reconocimiento de estructura
   - Mejor calidad en documentos complejos

2. **Tesseract** (Fallback)
   - Motor OCR tradicional
   - Rápido y ligero
   - Bueno para textos simples

3. **DocTR** (Alternativa Ligera)
   - Más rápido en CPU
   - Menor uso de memoria
   - Buena precisión general

## Arquitectura

El proyecto sigue una arquitectura hexagonal (puertos y adaptadores):

```
src/
├── config/        # Configuración y DI
├── domain/        # Lógica de negocio
├── infrastructure/# Adaptadores
└── interfaces/    # CLI y API
```

## Roadmap

### Sprint 1: Mejoras en el Procesamiento Core

#### 1.1 Procesamiento Paralelo
- [ ] Implementación de ProcessingService con soporte multithread
  ```python
  class ProcessingService:
      def process_batch(self, documents: List[Document], workers: int = 3)
      def process_async(self, document: Document) -> Future[Document]
  ```
- [ ] Cola de procesamiento con prioridades
- [ ] Sistema robusto de manejo de errores

#### 1.2 Mejoras OCR
- [ ] Preprocesamiento de imágenes
  - Detección automática de orientación
  - Corrección de sesgo
  - Mejora de contraste
- [ ] Detección inteligente de layouts
  - Reconocimiento de columnas
  - Identificación de tablas
  - Extracción de headers/footers
- [ ] Soporte multilenguaje
  - Detección automática de idioma
  - Diccionarios específicos por dominio

#### 1.3 Optimizaciones LLM
- [ ] Sistema de caché
  ```python
  class LlmCache:
      def get_cached_response(self, text_hash: str) -> Optional[str]
      def cache_response(self, text_hash: str, response: str)
  ```
- [ ] Prompts especializados por tipo de documento
- [ ] Sistema de fallback y reintentos

### Sprint 2: API y Almacenamiento

#### 2.1 API REST (FastAPI)
- [ ] Endpoints CRUD
  ```bash
  POST   /api/v1/documents      # Subir documento
  GET    /api/v1/documents      # Listar documentos
  GET    /api/v1/documents/{id} # Obtener documento
  DELETE /api/v1/documents/{id} # Eliminar documento
  ```
- [ ] Autenticación y autorización
- [ ] Documentación OpenAPI

#### 2.2 Sistema de Almacenamiento
- [ ] Soporte para S3
  ```python
  class S3Storage(StoragePort):
      def save_document(self, doc: Document) -> str
      def load_document(self, path: str) -> Document
  ```
- [ ] Versionado de documentos
- [ ] Gestión de caché

#### 2.3 Monitoreo
- [ ] Logging estructurado
- [ ] Métricas de rendimiento
- [ ] Sistema de alertas

### Sprint 3: Testing y CI/CD

#### 3.1 Testing Exhaustivo
- [ ] Tests de integración
  ```python
  def test_end_to_end_processing():
      # Probar flujo completo
  
  def test_error_handling():
      # Verificar manejo de errores
  ```
- [ ] Tests de rendimiento
- [ ] Mocks para servicios externos

#### 3.2 Pipeline CI/CD
- [ ] GitHub Actions
  ```yaml
  name: CI/CD Pipeline
  on: [push, pull_request]
  jobs:
    test:
      # Tests automatizados
    lint:
      # Análisis de código
    deploy:
      # Despliegue automático
  ```
- [ ] Análisis estático
- [ ] Despliegue automático

#### 3.3 Documentación
- [ ] API Reference
- [ ] Guías de uso
- [ ] Ejemplos prácticos

## Métricas de Éxito

1. **Rendimiento**
   - Tiempo de procesamiento < 30s por página
   - Precisión OCR > 95%
   - Latencia API < 100ms

2. **Calidad**
   - Cobertura de tests > 80%
   - Zero vulnerabilidades críticas
   - Documentación actualizada

## Configuración del Entorno

```bash
# Instalar dependencias
pip install -e ".[dev]"

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar tests
pytest tests/
```

## Configuración de Donut OCR

Donut (Document Understanding Transformer) es un modelo de IA avanzado para extracción de texto y comprensión de documentos. 

### Parámetros de Configuración

```python
# Configuración en .env
MODEL_NAME=naver-clova-ix/donut-base-finetuned-cord-v2  # Modelo pre-entrenado
USE_GPU=false                    # Usar GPU si está disponible
PDF_DPI=200                     # Resolución de escaneo
MAX_OUTPUT_LENGTH=1024          # Longitud máxima de salida
NUM_BEAMS=4                     # Número de beams para búsqueda
NUM_THREADS=4                   # Hilos para procesamiento
TEMPERATURE=0.8                 # Temperatura de generación
```

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit tus cambios
   ```bash
   git commit -m "feat(amazing): add something amazing"
   ```
4. Push a la rama
   ```bash
   git push origin feature/amazing-feature
   ```
5. Abre un Pull Request

## Convenciones

- **Commits**: Seguimos [Conventional Commits](https://www.conventionalcommits.org/)
- **Código**: [Black](https://github.com/psf/black) para formateo
- **Documentación**: Docstrings en Google style
- **Testing**: Pytest para todos los tests

## Licencia

Este proyecto está licenciado bajo MIT License - ver el archivo [LICENSE](LICENSE) para detalles.

## Agradecimientos

- OpenAI por la API GPT
- Tesseract OCR
- La comunidad de código abierto

---

No olvides dar una estrella si encuentras útil este proyecto!
