from typing import List, Optional
from pathlib import Path
import torch
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel
from pdf2image import convert_from_path

from domain.ports import OcrPort
from domain.models import Page, Document
from config.settings import Settings

class DonutAdapter(OcrPort):
    """Adaptador OCR usando el modelo Donut (Document Understanding Transformer)"""

    def __init__(self, settings: Settings):
        """Inicializa el adaptador Donut con la configuración especificada"""
        self.settings = settings
        self.model_name = "naver-clova-ix/donut-base-finetuned-cord-v2"
        self.processor = DonutProcessor.from_pretrained(self.model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
        
        # Mover a CPU/GPU según configuración
        self.device = "cuda" if torch.cuda.is_available() and settings.use_gpu else "cpu"
        self.model.to(self.device)
        
        self.task_prompt = "<s_docvqa><s_question>Extract text</s_question><s_answer>"

    def extract_text(self, image_path: str) -> str:
        """Extrae texto de una imagen usando Donut"""
        try:
            # Cargar y preparar la imagen
            image = Image.open(image_path).convert("RGB")
            pixel_values = self.processor(image, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)

            # Generar el texto
            outputs = self.model.generate(
                pixel_values,
                decoder_input_ids=self.processor.tokenizer(
                    self.task_prompt, return_tensors="pt"
                ).input_ids.to(self.device),
                max_length=self.settings.max_output_length,
                num_beams=self.settings.num_beams,
            )

            # Decodificar resultado
            result = self.processor.batch_decode(outputs, skip_special_tokens=True)[0]
            return result

        except Exception as e:
            raise OCRError(f"Error procesando imagen con Donut: {str(e)}")

    def process_pdf(self, pdf_path: Path) -> Document:
        """Procesa un PDF completo y retorna un Document con el texto extraído"""
        try:
            # Convertir PDF a imágenes
            pages = convert_from_path(
                pdf_path,
                dpi=self.settings.pdf_dpi,
                thread_count=self.settings.num_threads
            )

            # Procesar cada página
            processed_pages: List[Page] = []
            for idx, page_image in enumerate(pages, start=1):
                # Guardar imagen temporalmente
                temp_image_path = self.settings.temp_dir / f"page_{idx}.png"
                page_image.save(temp_image_path)

                # Extraer texto
                raw_text = self.extract_text(str(temp_image_path))
                processed_pages.append(Page(
                    number=idx,
                    raw_text=raw_text,
                    refined_text=None
                ))

                # Limpiar archivo temporal
                temp_image_path.unlink()

            return Document(
                name=pdf_path.name,
                pages=processed_pages,
                metadata={
                    "ocr_engine": "donut",
                    "model": "naver-clova/donut-base",
                    "dpi": self.settings.pdf_dpi
                }
            )

        except Exception as e:
            raise OCRError(f"Error procesando PDF con Donut: {str(e)}")

class OCRError(Exception):
    """Excepción específica para errores de OCR"""
    pass
