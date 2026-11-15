import asyncio
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from functools import lru_cache
import time
from cache import EmbeddingCache
from logger import logger

@lru_cache(maxsize=1)
def get_embedding_model():
    """Load and cache the embedding model"""
    return SentenceTransformer('all-MiniLM-L6-v2')

class BatchProcessor:
    """Batch processing for embeddings and database operations"""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, batch_size: int = 32, max_wait_time: float = 0.1):
        if not self._initialized:
            self.batch_size = batch_size
            self.max_wait_time = max_wait_time
            self.pending_queries = []
            self.pending_futures = []
            self.last_batch_time = time.time()
            self._initialized = True
    
    async def process_embedding_batch(self, queries: List[str]) -> List[np.ndarray]:
        """Process a batch of queries for embedding generation"""
        model = get_embedding_model()
        embeddings = model.encode(queries, convert_to_numpy=True)
        return embeddings
    
    async def get_embedding(self, query: str) -> np.ndarray:
        """Get embedding with batching support"""
        # Check cache first
        cached_embedding = await EmbeddingCache.get_embedding(query)
        if cached_embedding is not None:
            return cached_embedding
        
        # Add to batch
        future = asyncio.Future()
        self.pending_queries.append(query)
        self.pending_futures.append(future)
        
        # Process batch if conditions met
        current_time = time.time()
        if (len(self.pending_queries) >= self.batch_size or 
            current_time - self.last_batch_time > self.max_wait_time):
            await self._process_batch()
        
        return await future
    
    async def _process_batch(self):
        """Process the current batch of queries"""
        if not self.pending_queries:
            return
        
        queries = self.pending_queries.copy()
        futures = self.pending_futures.copy()
        
        # Clear pending
        self.pending_queries.clear()
        self.pending_futures.clear()
        self.last_batch_time = time.time()
        
        try:
            # Generate embeddings for batch
            embeddings = await self.process_embedding_batch(queries)
            
            # Cache embeddings
            for query, embedding in zip(queries, embeddings):
                await EmbeddingCache.set_embedding(query, embedding)
            
            # Resolve futures
            for future, embedding in zip(futures, embeddings):
                future.set_result(embedding)
                
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            for future in futures:
                future.set_exception(e)

async def startup_batch_processor():
    """Start background task for batch processing"""
    batch_processor = BatchProcessor()
    async def batch_processor_task():
        while True:
            await asyncio.sleep(0.05)  # 50ms check interval
            if batch_processor.pending_queries:
                current_time = time.time()
                if current_time - batch_processor.last_batch_time > batch_processor.max_wait_time:
                    await batch_processor._process_batch()
    asyncio.create_task(batch_processor_task())
