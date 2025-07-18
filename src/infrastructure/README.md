# Capa de Infraestructura

Esta carpeta contiene las implementaciones concretas (adaptadores) de las interfaces definidas en la capa de dominio.

## Archivos

### `openai_llm_adapter.py`

Implementación del puerto LLM usando la API de OpenAI.

```python
class OpenAIAdapter(LlmPort):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def refine(self, text: str) -> str:
        """Refina un texto usando el LLM"""
        # Implementación usando OpenAI API
    
    def batch_refine(self, texts: List[str]) -> List[str]:
        """Refina múltiples textos en batch"""
        # Implementación de procesamiento en batch
```

### `tesseract_adapter.py`

Implementación del puerto OCR usando Tesseract.

```python
class TesseractAdapter(OcrPort):
    def __init__(self, config: dict = None):
        self.config = config or {}
    
    def extract_text(self, image: bytes) -> str:
        """Extrae texto de una imagen usando Tesseract"""
        # Implementación usando pytesseract
```

### `file_storage.py`

Implementación del almacenamiento usando el sistema de archivos.

```python
class LocalFileStorage(StoragePort):
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    def save_document(self, doc: Document) -> str:
        """Guarda un documento procesado"""
        # Implementación de guardado en archivo
    
    def load_document(self, path: str) -> Document:
        """Carga un documento procesado"""
        # Implementación de carga desde archivo
```

## Responsabilidades

- Implementa las interfaces definidas en el dominio
- Maneja la integración con servicios externos
- Gestiona el almacenamiento de datos
- Encapsula los detalles técnicos específicos

## Configuración

Cada adaptador puede requerir configuración específica:

### OpenAI
```python
openai_config = {
    "api_key": "sk-your-key",
    "model": "gpt-4-turbo",
    "temperature": 0.2
}
```

### Tesseract
```python
tesseract_config = {
    "path": "/usr/bin/tesseract",
    "lang": "spa",
    "config": "--psm 1"
}
```

### Storage
```python
storage_config = {
    "base_path": "output/",
    "format": "markdown"
}
```
