# Configuración del Proyecto

Esta carpeta contiene la configuración y el contenedor de dependencias del proyecto.

## Archivos

### `settings.py`

Gestiona la configuración del proyecto usando `pydantic-settings`.

```python
class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str        # Clave API de OpenAI
    llm_model: str            # Modelo a usar (default: "gpt-4-turbo")
    llm_mode: LlmMode        # Modo de operación del LLM
    
    # OCR
    tesseract_path: str      # Ruta al ejecutable de Tesseract
    ocr_lang: str           # Idioma para OCR
    
    # Paths
    input_dir: Path         # Directorio de entrada
    output_dir: Path       # Directorio de salida
    
    # Processing
    batch_size: int        # Tamaño del batch para procesamiento
    max_retries: int      # Máximo número de reintentos
```

### `container.py`

Configura el contenedor de inyección de dependencias usando `dependency-injector`.

```python
class Container(containers.DeclarativeContainer):
    # Configuración
    config = providers.Configuration()
    
    # Servicios
    ocr_service = providers.Singleton(TesseractAdapter)
    llm_service = providers.Singleton(OpenAIAdapter)
    storage_service = providers.Singleton(FileStorageAdapter)
    
    # Casos de uso
    document_processor = providers.Singleton(DocumentProcessor)
```

## Variables de Entorno

El proyecto espera un archivo `.env` con las siguientes variables:

```env
OPENAI_API_KEY=sk-your-key-here
TESSERACT_PATH=/usr/bin/tesseract
OCR_LANG=spa
INPUT_DIR=pdfs
OUTPUT_DIR=output
BATCH_SIZE=5
MAX_RETRIES=3
```
