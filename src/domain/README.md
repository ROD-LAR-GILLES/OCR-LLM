# Capa de Dominio

Esta carpeta contiene la lógica de negocio central del proyecto, siguiendo los principios de Domain-Driven Design (DDD).

## Archivos

### `models.py`

Define las entidades principales del dominio.

```python
@dataclass
class Page:
    number: int           # Número de página
    raw_text: str        # Texto extraído por OCR
    refined_text: str    # Texto mejorado por LLM

@dataclass
class Document:
    name: str           # Nombre del documento
    pages: List[Page]   # Lista de páginas
    metadata: dict      # Metadatos adicionales
```

### `ports.py`

Define las interfaces (puertos) que la lógica de negocio requiere.

```python
class OcrPort(ABC):
    """Puerto para servicios de OCR"""
    @abstractmethod
    def extract_text(self, image: bytes) -> str: ...

class LlmPort(ABC):
    """Puerto para servicios de LLM"""
    @abstractmethod
    def refine(self, text: str) -> str: ...
    @abstractmethod
    def batch_refine(self, texts: List[str]) -> List[str]: ...

class StoragePort(ABC):
    """Puerto para almacenamiento"""
    @abstractmethod
    def save_document(self, doc: Document) -> str: ...
    @abstractmethod
    def load_document(self, path: str) -> Document: ...
```

### `use_cases.py`

Implementa los casos de uso de la aplicación.

```python
class DocumentProcessor:
    """Caso de uso principal para procesar documentos"""
    def __init__(self, ocr: OcrPort, llm: LlmPort, storage: StoragePort):
        self.ocr = ocr
        self.llm = llm
        self.storage = storage
    
    def process_document(self, request: ProcessDocumentRequest) -> Document:
        # Implementa el flujo principal de procesamiento
        pass
```

## Responsabilidades

- Define las entidades centrales del dominio
- Establece las interfaces para servicios externos
- Implementa la lógica de negocio en casos de uso
- No depende de implementaciones concretas (inversión de dependencias)
