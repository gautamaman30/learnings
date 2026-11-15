import asyncpg
import numpy as np
import json
import os 
from typing import List, Optional, Any, Dict

from models import VideoSegment

db_pool = None

async def init_database():
    """Initialize PostgreSQL database with required tables"""
    global db_pool

    db_pool = await asyncpg.create_pool(
        host=os.getenv('DB_HOST') or "localhost",
        port=os.getenv('DB_PORT') or 5432,
        user=os.getenv('DB_USERNAME') or "postgres",
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME') or "video_db",
        min_size=5,
        max_size=20
    )
    
    # Create tables
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE EXTENSION IF NOT EXISTS vector;
            
            CREATE TABLE IF NOT EXISTS video_segments (
                id SERIAL PRIMARY KEY,
                video_id VARCHAR(255) NOT NULL,
                start_timestamp FLOAT NOT NULL,
                end_timestamp FLOAT NOT NULL,
                text_content TEXT,
                embedding vector(384),  -- MiniLM embedding dimension
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_video_segments_video_id 
            ON video_segments(video_id);
            
            CREATE INDEX IF NOT EXISTS idx_video_segments_embedding 
            ON video_segments USING ivfflat (embedding vector_cosine_ops);
            
            CREATE INDEX IF NOT EXISTS idx_video_segments_timestamp 
            ON video_segments(video_id, start_timestamp);
        """)

class VideoDatabase:
    """Database operations for video segments"""

    @staticmethod
    async def insert_segments_batch(segments: List[VideoSegment]):
        """Insert multiple segments in batch"""
        async with db_pool.acquire() as conn:
            # Prepare data for batch insert
            insert_data = []
            for segment in segments:
                if segment.embedding:
                    embedding_str = f"[{','.join(map(str, segment.embedding))}]"
                else:
                    embedding_str = None
                
                insert_data.append((
                    segment.video_id,
                    segment.start_timestamp,
                    segment.end_timestamp,
                    segment.text_content,
                    embedding_str,
                    json.dumps(segment.metadata) if segment.metadata else None
                ))
            
            await conn.executemany("""
                INSERT INTO video_segments 
                (video_id, start_timestamp, end_timestamp, text_content, embedding, metadata)
                VALUES ($1, $2, $3, $4, $5::vector, $6)
            """, insert_data)
    
    @staticmethod
    async def search_similar_segments(
        query_embedding: np.ndarray,
        top_k: int = 5,
        video_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar segments using vector similarity"""
        async with db_pool.acquire() as conn:
            # Build query with optional video_id filter
            base_query = """
                SELECT video_id, start_timestamp, end_timestamp, text_content, 
                       metadata, 1 - (embedding <=> $1::vector) as similarity_score
                FROM video_segments
                WHERE embedding IS NOT NULL
            """
            
            params = [f"[{','.join(map(str, query_embedding))}]"]
            
            if video_ids:
                base_query += f" AND video_id = ANY($2)"
                params.append(video_ids)
            
            base_query += " ORDER BY similarity_score DESC LIMIT $" + str(len(params) + 1)
            params.append(top_k)
            
            rows = await conn.fetch(base_query, *params)
            
            return [
                {
                    'video_id': row['video_id'],
                    'start_timestamp': row['start_timestamp'],
                    'end_timestamp': row['end_timestamp'],
                    'text_content': row['text_content'],
                    'similarity_score': row['similarity_score'],
                    'metadata': row['metadata']
                }
                for row in rows
            ]
        
    @staticmethod
    async def get_video_embeddings_counts():
        async with db_pool.acquire() as conn:
            stats = await conn.fetchrow("""
                SELECT 
                    COUNT(*) as total_segments,
                    COUNT(DISTINCT video_id) as total_videos,
                    COUNT(*) FILTER (WHERE embedding IS NOT NULL) as segments_with_embeddings
                FROM video_segments
            """)
            
            return {
                "total_segments": stats['total_segments'],
                "total_videos": stats['total_videos'],
                "segments_with_embeddings": stats['segments_with_embeddings']
            }

async def close_database():
    if db_pool:
        await db_pool.close()