import asyncio
from typing import List, Dict
from datetime import datetime
from fastapi import HTTPException, BackgroundTasks
import time

from server import app
from logger import logger
from database import VideoDatabase
from services import BatchProcessor
from models import BatchProcessRequest, QueryRequest, QueryResult

@app.post("/api/segments/batch", response_model=Dict[str, str])
async def add_segments_batch(request: BatchProcessRequest, background_tasks: BackgroundTasks):
    """Add multiple video segments in batch"""
    try:
        # Process in background for better performance
        background_tasks.add_task(VideoDatabase.insert_segments_batch, request.segments)
        return {"message": f"Batch processing {len(request.segments)} segments"}
    except Exception as e:
        logger.error(f"Batch insert failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process segments")

@app.post("/api/query", response_model=List[QueryResult])
async def query_videos(request: QueryRequest):
    """Query videos for most relevant segments"""
    start_time = time.time()
    
    try:
        # Get query embedding with batching
        batch_processor = BatchProcessor()
        query_embedding = await batch_processor.get_embedding(request.query)
        
        # Search similar segments
        results = await VideoDatabase.search_similar_segments(
            query_embedding,
            top_k=request.top_k,
            video_ids=request.video_ids
        )
        
        # Convert to response format
        response = [
            QueryResult(
                video_id=result['video_id'],
                start_timestamp=result['start_timestamp'],
                end_timestamp=result['end_timestamp'],
                text_content=result['text_content'],
                similarity_score=result['similarity_score'],
                metadata=result['metadata']
            )
            for result in results
        ]
        
        processing_time = time.time() - start_time
        logger.info(f"Query processed in {processing_time:.3f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail="Query processing failed")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        stats = VideoDatabase.get_video_embeddings_counts()
        if stats:
            return stats
    except Exception as e:
        logger.error(f"Stats query failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stats")

