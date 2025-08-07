import re
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class QualityMetrics:
    confidence_score: float
    text_length: int
    word_count: int
    special_char_ratio: float
    readability_score: float
    has_corrupted_output: bool

class DocumentQualityService:
    def __init__(self):
        self.min_confidence = 0.7
        self.max_special_char_ratio = 0.3
    
    def assess_quality(self, text: str, confidence: float = None) -> QualityMetrics:
        """Evalúa la calidad del texto extraído"""
        
        # Detectar salida corrupta típica de Donut
        corrupted_patterns = [
            r'<sep/>.*<sep/>',  # Separadores repetitivos
            r'(\S)\1{20,}',     # Caracteres repetitivos
            r'[가-힣]{10,}',     # Texto coreano extenso
            r'^\s*$',           # Texto vacío
            r'^\W+$'            # Solo caracteres especiales
        ]
        
        has_corrupted = any(re.search(pattern, text) for pattern in corrupted_patterns)
        
        # Métricas básicas
        word_count = len(text.split())
        text_length = len(text)
        special_chars = len(re.findall(r'[^\w\s]', text))
        special_char_ratio = special_chars / max(text_length, 1)
        
        # Puntuación de legibilidad simple
        if word_count == 0:
            readability_score = 0.0
        else:
            avg_word_length = text_length / word_count
            readability_score = min(1.0, 1 / (1 + abs(avg_word_length - 5) * 0.1))
        
        return QualityMetrics(
            confidence_score=confidence or 0.5,
            text_length=text_length,
            word_count=word_count,
            special_char_ratio=special_char_ratio,
            readability_score=readability_score,
            has_corrupted_output=has_corrupted
        )
    
    def should_retry(self, metrics: QualityMetrics) -> bool:
        """Determina si se debe reintentar el procesamiento"""
        return (
            metrics.has_corrupted_output or
            metrics.confidence_score < self.min_confidence or
            metrics.special_char_ratio > self.max_special_char_ratio or
            metrics.word_count < 5
        )