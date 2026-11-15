import redis.asyncio as redis
import hashlib
import os 
import numpy as np

from typing import Optional
from logger import logger

redis_client = None

async def init_redis():
    """Initialize Redis for caching"""
    global redis_client

    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        password=os.getenv('REDIS_PASSWORD'),
        decode_responses=False  # Keep binary for numpy arrays
    )

class EmbeddingCache:
    """Cache for query embeddings"""
    
    @staticmethod
    def _get_cache_key(query: str) -> str:
        """Generate cache key for query"""
        return f"embedding:{hashlib.md5(query.encode()).hexdigest()}"
    
    @staticmethod
    async def get_embedding(query: str) -> Optional[np.ndarray]:
        """Get cached embedding for query"""
        try:
            key = EmbeddingCache._get_cache_key(query)
            cached = await redis_client.get(key)
            if cached:
                return np.frombuffer(cached, dtype=np.float32)
        except Exception as e:
            logger.warning(f"Cache get failed: {e}")
        return None
    
    @staticmethod
    async def set_embedding(query: str, embedding: np.ndarray, ttl: int = 3600):
        """Cache embedding for query"""
        try:
            key = EmbeddingCache._get_cache_key(query)
            await redis_client.setex(key, ttl, embedding.tobytes())
        except Exception as e:
            logger.warning(f"Cache set failed: {e}")

async def close_redis():
    if redis_client:
        await redis_client.close()