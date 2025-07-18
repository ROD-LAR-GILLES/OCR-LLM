"""
Puerto para el sistema de monitoreo y observabilidad.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime

class MonitoringPort(ABC):
    """
    Puerto abstracto para implementaciones de monitoreo.
    Define las operaciones básicas que debe soportar cualquier sistema de monitoreo.
    """
    
    @abstractmethod
    def start_operation(self, operation_name: str, context: Dict[str, Any]) -> str:
        """
        Inicia el rastreo de una operación.
        
        Args:
            operation_name: Nombre de la operación
            context: Contexto de la operación
            
        Returns:
            str: Identificador de la operación
        """
        pass
    
    @abstractmethod
    def end_operation(self, operation_id: str, status: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Finaliza el rastreo de una operación.
        
        Args:
            operation_id: Identificador de la operación
            status: Estado final de la operación
            metadata: Metadatos adicionales
        """
        pass
    
    @abstractmethod
    def record_metric(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """
        Registra una métrica.
        
        Args:
            name: Nombre de la métrica
            value: Valor de la métrica
            labels: Etiquetas adicionales
        """
        pass
    
    @abstractmethod
    def record_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """
        Registra un error.
        
        Args:
            error: Excepción ocurrida
            context: Contexto del error
        """
        pass
