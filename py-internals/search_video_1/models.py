from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class VideoSegment(BaseModel):
    video_id: str
    start_timestamp: float
    end_timestamp: float
    text_content: str
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    video_ids: Optional[List[str]] = None  # Filter by specific videos

class QueryResult(BaseModel):
    video_id: str
    start_timestamp: float
    end_timestamp: float
    text_content: str
    similarity_score: float
    metadata: Optional[Dict[str, Any]] = None

class BatchProcessRequest(BaseModel):
    segments: List[VideoSegment]