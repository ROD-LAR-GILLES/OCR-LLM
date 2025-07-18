"""
Modelos de dominio para el procesamiento de documentos.

Este módulo define las estructuras de datos principales utilizadas en el sistema
para representar documentos y sus páginas procesadas por Donut.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Page:
    """
    Representa una página individual de un documento procesado.
    
    Esta clase almacena el contenido extraído de una página, incluyendo
    el texto original extraído por Donut y cualquier metadata asociada.
    
    Attributes:
        number (int): Número de página en el documento original
        raw_text (str): Texto extraído directamente por Donut, incluyendo
                       cualquier estructura o formato detectado
        refined_text (Optional[str]): Texto procesado o estructurado,
                                    si se ha aplicado algún procesamiento adicional
    
    Example:
        >>> page = Page(number=1, raw_text="Contenido extraído...")
        >>> print(page.number)
        1
    """
    number: int
    raw_text: str
    refined_text: Optional[str] = None

@dataclass
class Document:
    """
    Representa un documento completo procesado por el sistema.
    
    Mantiene la colección de páginas procesadas junto con metadata
    del documento y configuración utilizada en el procesamiento.
    
    Attributes:
        name (str): Nombre del documento original (ej: "documento.pdf")
        pages (List[Page]): Lista de páginas procesadas del documento
        metadata (Dict): Información adicional sobre el documento y su procesamiento.
                      Puede incluir:
                      - processor: Motor de OCR utilizado (ej: "donut")
                      - model: Modelo específico usado
                      - timestamp: Fecha y hora del procesamiento
                      - settings: Configuración utilizada
    
    Example:
        >>> doc = Document(
        ...     name="ejemplo.pdf",
        ...     pages=[Page(number=1, raw_text="Contenido...")],
        ...     metadata={"processor": "donut", "model": "donut-base-finetuned"}
        ... )
        >>> print(len(doc.pages))
        1
    """
    name: str
    pages: List[Page]
    metadata: Dict