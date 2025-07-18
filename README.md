# OCR-LLM: Procesamiento de Documentos con OCR y LLM

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
