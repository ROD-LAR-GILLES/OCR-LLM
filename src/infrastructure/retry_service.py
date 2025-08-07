import asyncio
import time
from typing import Callable, Any, Optional
from functools import wraps
from src.domain.exceptions import RetryableError
import structlog

logger = structlog.get_logger(__name__)

class RetryService:
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
    
    async def execute_with_retry(
        self, 
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Ejecuta función con reintentos exponenciales"""
        last_exception = None
        
        for attempt in range(1, self.max_attempts + 1):
            try:
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                
                if attempt > 1:
                    logger.info("retry_success", attempt=attempt, function=func.__name__)
                
                return result
                
            except RetryableError as e:
                last_exception = e
                if attempt < self.max_attempts:
                    delay = self.base_delay * (2 ** (attempt - 1))
                    logger.warning(
                        "retry_attempt", 
                        attempt=attempt, 
                        max_attempts=self.max_attempts,
                        delay=delay,
                        error=str(e)
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error("retry_exhausted", attempts=attempt, error=str(e))
            
            except Exception as e:
                # No reintentar errores no recuperables
                logger.error("non_retryable_error", error=str(e), function=func.__name__)
                raise
        
        raise last_exception

def retry_on_failure(max_attempts: int = 3, base_delay: float = 1.0):
    """Decorator para reintentos automáticos"""
    def decorator(func):
        retry_service = RetryService(max_attempts, base_delay)
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await retry_service.execute_with_retry(func, *args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return asyncio.run(retry_service.execute_with_retry(func, *args, **kwargs))
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator