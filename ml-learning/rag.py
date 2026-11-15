import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import nltk
from nltk.tokenize import sent_tokenize
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentProcessor:    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def process_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if not text or not text.strip():
            return []
            
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                words = current_chunk.split()
                overlap_text = " ".join(words[-self.chunk_overlap:]) if len(words) > self.chunk_overlap else ""
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        result = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "text": chunk,
                "chunk_id": i
            }
            if metadata:
                chunk_data.update(metadata)
                
            result.append(chunk_data)
            
        logger.info(f"Processed document into {len(result)} chunks")
        return result

class EmbeddingGenerator:    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        logger.info(f"Generating embeddings for {len(texts)} chunks")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

class VectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = None
        
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: np.ndarray):
        self.documents.extend(documents)
        
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack((self.embeddings, embeddings))
            
        logger.info(f"Added {len(documents)} documents to vector store. Total documents: {len(self.documents)}")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        if self.embeddings is None or len(self.documents) == 0:
            logger.warning("Vector store is empty")
            return []
        
        # Reshape query embedding to (1, dim)
        query_embedding = query_embedding.reshape(1, -1)
        
        # Calculate cosine similarity between query and all documents
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get indices of top_k most similar documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "similarity": float(similarities[idx])
            })
        
        logger.info(f"Found {len(results)} documents for query")
        return results

class Generator:
    """Generate responses based on retrieved documents using an LLM."""
    
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        logger.info(f"Loading language model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
    def generate(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """
        Generate a response to the query based on the retrieved documents.
        
        Args:
            query: User query
            context_docs: List of retrieved document dictionaries
            
        Returns:
            Generated response
        """
        # Format context from retrieved documents
        context = "\n\n".join([doc["document"]["text"] for doc in context_docs])
        
        # Create prompt with context and query
        prompt = f"""
You are a helpful AI assistant. Answer the question based on the following context:

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""
        
        # Generate response
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=1536,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            num_return_sequences=1
        )
        
        # Decode the response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the answer part
        if "ANSWER:" in response:
            response = response.split("ANSWER:")[-1].strip()
            
        logger.info(f"Generated response of length {len(response)}")
        return response

class RAGSystem:
    """Complete RAG system combining document processing, embedding, retrieval, and generation."""
    
    def __init__(
        self, 
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ):
        logger.info("Initializing RAG system")
        self.doc_processor = DocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embedding_generator = EmbeddingGenerator(model_name=embedding_model)
        self.vector_store = VectorStore()
        self.generator = Generator(model_name=llm_model)
    
    def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        if metadatas is None:
            metadatas = [{} for _ in texts]
            
        all_chunks = []

        for i, (text, metadata) in enumerate(zip(texts, metadatas)):
            doc_metadata = {"doc_id": i, **metadata}
            chunks = self.doc_processor.process_text(text, doc_metadata)
            all_chunks.extend(chunks)
        
        chunk_texts = [chunk["text"] for chunk in all_chunks]
        embeddings = self.embedding_generator.generate_embeddings(chunk_texts)
        
        self.vector_store.add_documents(all_chunks, embeddings)
        
        logger.info(f"Added {len(texts)} documents with {len(all_chunks)} total chunks")
    
    def query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        logger.info(f"Processing query: {query}")

        query_embedding = self.embedding_generator.generate_embeddings([query])[0]        
        retrieved_docs = self.vector_store.search(query_embedding, top_k=top_k)
        response = self.generator.generate(query, retrieved_docs)
        
        return {
            "query": query,
            "response": response,
            "retrieved_documents": retrieved_docs
        }

def demo_rag_system():
    rag = RAGSystem(
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        llm_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    )
    
    documents = [
        """Artificial intelligence (AI) is intelligence demonstrated by machines. It includes machine learning, where computers improve at tasks with experience. 
        Deep learning is a subset of machine learning using neural networks with many layers. AI applications include natural language processing, computer vision, 
        and recommendation systems. Ethical concerns include bias, privacy, and job displacement.""",
        
        """Machine learning is a field of artificial intelligence that enables computers to learn from data without being explicitly programmed. 
        Supervised learning uses labeled data, while unsupervised learning finds patterns in unlabeled data. Reinforcement learning involves agents 
        learning optimal actions through trial and error. Popular algorithms include decision trees, support vector machines, and neural networks.""",
        
        """Natural Language Processing (NLP) combines linguistics and machine learning to help computers understand human language. 
        Tasks include sentiment analysis, named entity recognition, and question answering. Transformer models like BERT and GPT have 
        revolutionized NLP by capturing contextual relationships in text. Applications include chatbots, translation services, and text summarization.""",
        
        """Computer vision enables computers to derive information from digital images and videos. Techniques include image classification, 
        object detection, and segmentation. Convolutional Neural Networks (CNNs) are the backbone of modern computer vision systems. 
        Applications include facial recognition, autonomous vehicles, and medical image analysis."""
    ]
    
    rag.add_documents(
        texts=documents, 
        metadatas=[
            {"title": "Introduction to AI", "source": "AI Textbook"},
            {"title": "Machine Learning Basics", "source": "ML Course"},
            {"title": "NLP Overview", "source": "NLP Guide"},
            {"title": "Computer Vision Fundamentals", "source": "CV Tutorial"}
        ]
    )
    
    query = "What are some applications of natural language processing?"
    result = rag.query(query, top_k=3)
    
    # Print the results
    print("\nQuery:", query)
    print("\nResponse:", result["response"])
    print("\nRetrieved Documents:")
    for i, doc in enumerate(result["retrieved_documents"]):
        print(f"\n{i+1}. Document (Similarity: {doc['similarity']:.4f}):")
        print(f"   Title: {doc['document'].get('title', 'No title')}")
        print(f"   Source: {doc['document'].get('source', 'No source')}")
        print(f"   Text snippet: {doc['document']['text'][:100]}...")

if __name__ == "__main__":
    demo_rag_system()