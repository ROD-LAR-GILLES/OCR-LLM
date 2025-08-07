from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
from PIL import Image
import re

class ImprovedDonutAdapter(OcrPort):
    def __init__(self, settings: Settings):
        self.settings = settings
        # Usar modelo específico para documentos en español
        self.model_name = "naver-clova-ix/donut-base-finetuned-docvqa"
        self.processor = DonutProcessor.from_pretrained(self.model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
        
        self.device = "cuda" if torch.cuda.is_available() and settings.use_gpu else "cpu"
        self.model.to(self.device)
        
        # Prompts mejorados para diferentes tipos de documentos
        self.task_prompts = {
            "general": "<s_docvqa><s_question>What is the text in this document?</s_question><s_answer>",
            "table": "<s_docvqa><s_question>Extract table data</s_question><s_answer>",
            "form": "<s_docvqa><s_question>Extract form fields and values</s_question><s_answer>"
        }
    
    def extract_text(self, image_path: str, document_type: str = "general") -> str:
        """Extrae texto con mejor manejo de prompts y postprocesamiento"""
        try:
            image = Image.open(image_path).convert("RGB")
            
            # Preprocessar imagen para mejor calidad
            image = self._preprocess_image(image)
            
            pixel_values = self.processor(image, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)
            
            prompt = self.task_prompts.get(document_type, self.task_prompts["general"])
            decoder_input_ids = self.processor.tokenizer(
                prompt, 
                return_tensors="pt",
                add_special_tokens=False
            ).input_ids.to(self.device)
            
            # Parámetros optimizados para mejor calidad
            outputs = self.model.generate(
                pixel_values,
                decoder_input_ids=decoder_input_ids,
                max_length=self.settings.max_output_length,
                num_beams=self.settings.num_beams,
                temperature=0.1,  # Más determinístico
                do_sample=False,
                early_stopping=True,
                pad_token_id=self.processor.tokenizer.pad_token_id,
                eos_token_id=self.processor.tokenizer.eos_token_id
            )
            
            # Decodificar y limpiar resultado
            result = self.processor.batch_decode(outputs, skip_special_tokens=True)[0]
            cleaned_text = self._postprocess_text(result, prompt)
            
            return cleaned_text
            
        except Exception as e:
            raise OCRError(f"Error procesando imagen con Donut: {str(e)}")
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocesa imagen para mejor OCR"""
        # Redimensionar si es muy grande
        max_size = 2048
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Convertir a escala de grises si es necesario para mejor contraste
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        return image
    
    def _postprocess_text(self, raw_text: str, prompt: str) -> str:
        """Limpia y mejora el texto extraído"""
        # Remover el prompt de la salida
        text = raw_text.replace(prompt, "").strip()
        
        # Remover tokens especiales y separadores
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'<sep/>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remover caracteres repetitivos
        text = re.sub(r'(\S)\1{10,}', r'\1', text)
        
        # Limpiar líneas vacías múltiples
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()