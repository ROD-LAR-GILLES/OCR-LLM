from dataclasses import dataclass
from typing import Protocol
from .models import Document
from .ports import OcrPort, PdfPort, LlmPort, StoragePort

@dataclass
class ProcessDocumentRequest:
    pdf_path: str
    output_format: str = "markdown"
    batch_size: int = 5

class DocumentProcessor:
    def __init__(
        self,
        pdf_service: PdfPort,
        ocr_service: OcrPort,
        llm_service: LlmPort,
        storage: StoragePort
    ):
        self.pdf_service = pdf_service
        self.ocr_service = ocr_service
        self.llm_service = llm_service
        self.storage = storage

    def process_document(self, request: ProcessDocumentRequest) -> Document:
        # 1. Extraer páginas del PDF
        page_images = self.pdf_service.extract_pages(request.pdf_path)
        
        # 2. Procesar OCR en cada página
        pages = []
        for i, image in enumerate(page_images):
            raw_text = self.ocr_service.extract_text(image)
            pages.append(Page(number=i+1, raw_text=raw_text))
            
        # 3. Crear documento
        document = Document(
            name=request.pdf_path,
            pages=pages,
            metadata={"format": request.output_format}
        )
        
        # 4. Refinar texto con LLM en batches
        for i in range(0, len(document.pages), request.batch_size):
            batch = document.pages[i:i + request.batch_size]
            raw_texts = [p.raw_text for p in batch]
            refined_texts = self.llm_service.batch_refine(raw_texts)
            for page, refined in zip(batch, refined_texts):
                page.refined_text = refined
        
        # 5. Guardar resultado
        self.storage.save_document(document)
        
        return document		
		