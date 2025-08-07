"""
Implementación del adaptador de caché usando Redis.
"""
import json
import hashlib
from typing import Optional, Any
from datetime import timedelta
import redis.asyncio as redis
from domain.cache_port import CachePort

class RedisCache(CachePort):
    """
    Implementación de CachePort usando Redis como backend.
    """
    
    def __init__(self, redis_url: str, ttl_hours: int = 24):
        """
        Inicializa la conexión con Redis.
        
        Args:
            redis_url: URL de conexión a Redis (redis://localhost:6379)
            ttl_hours: Tiempo de vida por defecto en horas (opcional, por defecto 24)
        """
        self.client = redis.from_url(redis_url)
        self.ttl_seconds = ttl_hours * 3600
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Recupera un valor del caché de Redis.
        
        Args:
            key: Clave a buscar
            
        Returns:
            Optional[Any]: Valor deserializado o None si no existe
        """
        value = await self.client.get(key)
        if value is None:
            return None
        return json.loads(value)
        
    async def set(self, key: str, value: Any, ttl: Optional[timedelta] = None) -> bool:
        """
        Almacena un valor en Redis.
        
        Args:
            key: Clave para almacenar el valor
            value: Valor a almacenar (será serializado a JSON)
            ttl: Tiempo de vida del valor en caché
            
        Returns:
            bool: True si se almacenó correctamente
        """
        serialized = json.dumps(value)
        if ttl:
            return await self.client.setex(key, int(ttl.total_seconds()), serialized)
        return await self.client.set(key, serialized)
        
    async def delete(self, key: str) -> bool:
        """
        Elimina un valor de Redis.
        
        Args:
            key: Clave a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return await self.client.delete(key) > 0
        
    async def exists(self, key: str) -> bool:
        """
        Verifica si una clave existe en Redis.
        
        Args:
            key: Clave a verificar
            
        Returns:
            bool: True si la clave existe
        """
        return await self.client.exists(key) > 0
    
    def get_cached_result(self, content_hash: str) -> Optional[str]:
        """Obtiene resultado del caché"""
        try:
            result = self.client.get(f"ocr:{content_hash}")
            return result.decode() if result else None
        except Exception:
            return None
    
    def cache_result(self, content_hash: str, result: str) -> None:
        """Guarda resultado en caché"""
        try:
            self.client.setex(
                f"ocr:{content_hash}", 
                self.ttl_seconds, 
                result
            )
        except Exception:
            pass  # Fallar silenciosamente si no hay Redis
    
    def generate_hash(self, content: bytes) -> str:
        """Genera hash para contenido"""
        return hashlib.sha256(content).hexdigest()

    async def close(self):
        """
        Cierra la conexión con Redis.
        """
        await self.client.close()
