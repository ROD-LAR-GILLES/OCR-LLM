# src/infrastructure/openai_llm_adapter.py
from openai import OpenAI
from domain.ports import LlmPort

class OpenAIAdapter(LlmPort):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
    def refine(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
        
    def batch_refine(self, texts: list[str]) -> list[str]:
        # Implementar procesamiento en batch para optimizar
        return [self.refine(text) for text in texts]
        
    def _get_system_prompt(self) -> str:
        return """Eres un experto en mejorar y formatear texto extraído por OCR.
                 Tu tarea es corregir errores comunes de OCR y mejorar la legibilidad
                 del texto manteniendo su significado original."""