#!/usr/bin/env python3
"""
Script minimalista para OCR usando Donut.
Optimizado para Mac M1/M2.
"""
import os
from pathlib import Path
from typing import List

import torch
from pdf2image import convert_from_path
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel

class DonutOCR:
    def __init__(self, model_name: str = "naver-clova-ix/donut-base"):
        """Inicializa Donut con el modelo especificado"""
        self.processor = DonutProcessor.from_pretrained(model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        
        # Usar CPU en Mac M1/M2 por ahora
        self.device = "cpu"
        self.model.to(self.device)
        
        # Prompt básico para extracción de texto
        self.task_prompt = "<s_docvqa><s_question>Extract text</s_question><s_answer>"

    def extract_text(self, image: Image.Image) -> str:
        """Extrae texto de una imagen usando Donut"""
        # Preparar imagen
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)

        # Generar texto
        outputs = self.model.generate(
            pixel_values,
            decoder_input_ids=self.processor.tokenizer(
                self.task_prompt, return_tensors="pt"
            ).input_ids.to(self.device),
            max_length=1024,
            num_beams=4,
        )

        # Decodificar y retornar
        return self.processor.batch_decode(outputs, skip_special_tokens=True)[0]

    def process_pdf(self, pdf_path: str, output_format: str = "text") -> List[str]:
        """Procesa un PDF y retorna el texto de cada página"""
        # Convertir PDF a imágenes
        pages = convert_from_path(
            pdf_path,
            dpi=200,  # Ajusta según necesites
        )

        # Procesar cada página
        results = []
        for i, page_image in enumerate(pages, 1):
            print(f"Procesando página {i}/{len(pages)}...")
            text = self.extract_text(page_image)
            results.append(text)

        return results

def main():
    # Obtener ruta del PDF desde argumentos
    import sys
    if len(sys.argv) < 2:
        print("Error: Debe proporcionar la ruta al archivo PDF")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    print("Inicializando Donut OCR...")
    ocr = DonutOCR()
    
    print(f"Procesando {pdf_path}...")
    texts = ocr.process_pdf(pdf_path)
    
    # Guardar resultados
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "resultado.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for i, text in enumerate(texts, 1):
            f.write(f"=== Página {i} ===\n{text}\n\n")
    
    print(f"Resultados guardados en {output_file}")

if __name__ == "__main__":
    main()
