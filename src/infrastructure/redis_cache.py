"""
Implementación del adaptador de caché usando Redis.
"""
import json
from typing import Optional, Any
from datetime import timedelta
import redis.asyncio as redis
from domain.cache_port import CachePort

class RedisCache(CachePort):
    """
    Implementación de CachePort usando Redis como backend.
    """
    
    def __init__(self, redis_url: str):
        """
        Inicializa la conexión con Redis.
        
        Args:
            redis_url: URL de conexión a Redis (redis://localhost:6379)
        """
        self.redis = redis.from_url(redis_url)
        
    async def get(self, key: str) -> Optional[Any]:
        """
        Recupera un valor del caché de Redis.
        
        Args:
            key: Clave a buscar
            
        Returns:
            Optional[Any]: Valor deserializado o None si no existe
        """
        value = await self.redis.get(key)
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
            return await self.redis.setex(key, int(ttl.total_seconds()), serialized)
        return await self.redis.set(key, serialized)
        
    async def delete(self, key: str) -> bool:
        """
        Elimina un valor de Redis.
        
        Args:
            key: Clave a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return await self.redis.delete(key) > 0
        
    async def exists(self, key: str) -> bool:
        """
        Verifica si una clave existe en Redis.
        
        Args:
            key: Clave a verificar
            
        Returns:
            bool: True si la clave existe
        """
        return await self.redis.exists(key) > 0
        
    async def close(self):
        """
        Cierra la conexión con Redis.
        """
        await self.redis.close()
