from contextlib import asynccontextmanager
from fastapi import FastAPI

from logger import logger
from cache import init_redis, close_redis
from database import init_database, close_database
from services import get_embedding_model, startup_batch_processor

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    
    logger.info("Starting up video retrieval system...")
    await init_database()
    await init_redis()

    await startup_batch_processor()
    
    model = get_embedding_model()
    logger.info("System ready!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    close_database()
    close_redis()

app = FastAPI(
    title="Video Retrieval System",
    description="Fast video segment retrieval with timestamp precision",
    version="1.0.0",
    lifespan=lifespan
)