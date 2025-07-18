from dataclasses import dataclass
from typing import List

@dataclass
class Page:
    number: int
    raw_text: str
    refined_text: str | None = None

@dataclass
class Document:
    name: str
    pages: List[Page]
    metadata: dict