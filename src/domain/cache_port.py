"""
Puerto para el sistema de caché.
"""
from abc import ABC, abstractmethod
from typing import Optional, Any
from datetime import timedelta

class CachePort(ABC):
    """
    Puerto abstracto para implementaciones de caché.
    Define las operaciones básicas que debe soportar cualquier caché.
    """
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """
        Recupera un valor del caché.
        
        Args:
            key: Clave a buscar
            
        Returns:
            Optional[Any]: Valor almacenado o None si no existe
        """
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[timedelta] = None) -> bool:
        """
        Almacena un valor en el caché.
        
        Args:
            key: Clave para almacenar el valor
            value: Valor a almacenar
            ttl: Tiempo de vida del valor en caché
            
        Returns:
            bool: True si se almacenó correctamente
        """
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """
        Elimina un valor del caché.
        
        Args:
            key: Clave a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        Verifica si una clave existe en el caché.
        
        Args:
            key: Clave a verificar
            
        Returns:
            bool: True si la clave existe
        """
        pass
