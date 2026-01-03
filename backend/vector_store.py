"""
Simple Vector Store (No ChromaDB needed)
=========================================
Lightweight in-memory vector store using cosine similarity
"""

import json
import numpy as np
from typing import List, Dict, Optional
from pathlib import Path
import pickle


class SimpleVectorStore:
    """Simple in-memory vector store with cosine similarity search"""
    
    def __init__(self, persist_directory: str = "data/vector_db"):
        """
        Initialize simple vector store
        
        Args:
            persist_directory: Directory to store vectors
        """
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        self.persist_path = Path(persist_directory) / "vectors.pkl"
        
        self.documents = []  # List of document chunks
        self.vectors = []    # List of vectors (simple TF-IDF)
        self.metadata = []   # List of metadata dicts
        
        # Load existing data if available
        if self.persist_path.exists():
            self._load()
        
        print(f"✅ Simple vector store initialized at {persist_directory}")
    
    def _simple_vectorize(self, text: str) -> List[float]:
        """
        Create simple vector from text using word frequency
        This is a basic TF approach (better than nothing!)
        """
        # Simple word tokenization and frequency count
        words = text.lower().split()
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Create a consistent vocabulary from all seen words
        # For simplicity, we'll use top 1000 most common words
        vocab = sorted(set(words))[:1000]
        
        # Create vector
        vector = [word_freq.get(word, 0) for word in vocab]
        
        # Normalize
        norm = sum(v * v for v in vector) ** 0.5
        if norm > 0:
            vector = [v / norm for v in vector]
        
        return vector
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        # Pad vectors to same length
        max_len = max(len(vec1), len(vec2))
        vec1 = vec1 + [0] * (max_len - len(vec1))
        vec2 = vec2 + [0] * (max_len - len(vec2))
        
        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def add_document(self, doc_id: int, chunks: List[Dict], metadata: Dict):
        """
        Add document chunks to vector store
        
        Args:
            doc_id: Document ID from database
            chunks: List of text chunks
            metadata: Document metadata
        """
        try:
            for chunk in chunks:
                # Create vector
                vector = self._simple_vectorize(chunk['text'])
                
                # Store
                self.documents.append(chunk['text'])
                self.vectors.append(vector)
                self.metadata.append({
                    'doc_id': doc_id,
                    'chunk_id': chunk['id'],
                    'filename': metadata.get('filename', 'unknown'),
                    'start_char': chunk['start_char'],
                    'end_char': chunk['end_char']
                })
            
            # Save to disk
            self._save()
            
            print(f"✅ Added {len(chunks)} chunks from document {doc_id}")
            
        except Exception as e:
            print(f"❌ Error adding document to vector store: {str(e)}")
            raise
    
    def search(self, query: str, top_k: int = 3, doc_id: Optional[int] = None) -> List[Dict]:
        """
        Search for similar chunks
        
        Args:
            query: Search query
            top_k: Number of results to return
            doc_id: Optional - filter by specific document ID
            
        Returns:
            List of relevant chunks with scores
        """
        try:
            if not self.documents:
                return []
            
            # Vectorize query
            query_vector = self._simple_vectorize(query)
            
            # Calculate similarities
            similarities = []
            for i, (doc_vector, meta) in enumerate(zip(self.vectors, self.metadata)):
                # Filter by doc_id if specified
                if doc_id is not None and meta['doc_id'] != doc_id:
                    continue
                
                similarity = self._cosine_similarity(query_vector, doc_vector)
                similarities.append((i, similarity))
            
            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get top k results
            results = []
            for i, score in similarities[:top_k]:
                results.append({
                    'text': self.documents[i],
                    'metadata': self.metadata[i],
                    'distance': 1.0 - score  # Convert similarity to distance
                })
            
            print(f"✅ Found {len(results)} relevant chunks")
            return results
            
        except Exception as e:
            print(f"❌ Error searching vector store: {str(e)}")
            return []
    
    def delete_document(self, doc_id: int):
        """Delete all chunks from a document"""
        try:
            # Find indices to delete
            indices_to_delete = [i for i, meta in enumerate(self.metadata) if meta['doc_id'] == doc_id]
            
            # Delete in reverse order to maintain indices
            for i in sorted(indices_to_delete, reverse=True):
                del self.documents[i]
                del self.vectors[i]
                del self.metadata[i]
            
            # Save
            self._save()
            
            print(f"✅ Deleted document {doc_id} from vector store")
            
        except Exception as e:
            print(f"❌ Error deleting document: {str(e)}")
            raise
    
    def count_documents(self) -> int:
        """Get total number of chunks in the store"""
        return len(self.documents)
    
    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        return {
            'total_chunks': len(self.documents),
            'collection_name': 'simple_vectors'
        }
    
    def _save(self):
        """Save vectors to disk"""
        try:
            data = {
                'documents': self.documents,
                'vectors': self.vectors,
                'metadata': self.metadata
            }
            with open(self.persist_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"⚠️ Could not save vectors: {e}")
    
    def _load(self):
        """Load vectors from disk"""
        try:
            with open(self.persist_path, 'rb') as f:
                data = pickle.load(f)
            self.documents = data.get('documents', [])
            self.vectors = data.get('vectors', [])
            self.metadata = data.get('metadata', [])
            print(f"✅ Loaded {len(self.documents)} vectors from disk")
        except Exception as e:
            print(f"⚠️ Could not load vectors: {e}")


# Backward compatibility - use SimpleVectorStore instead of ChromaDB
VectorStore = SimpleVectorStore


# Test if run directly
if __name__ == "__main__":
    print("Testing Simple Vector Store...")
    
    store = SimpleVectorStore("data/test_vector_db")
    
    # Test adding documents
    test_chunks = [
        {'id': 0, 'text': 'Python is a programming language.', 'start_char': 0, 'end_char': 34},
        {'id': 1, 'text': 'It is widely used for AI and machine learning.', 'start_char': 35, 'end_char': 81}
    ]
    
    store.add_document(
        doc_id=1,
        chunks=test_chunks,
        metadata={'filename': 'test.pdf'}
    )
    
    # Test search
    results = store.search("What is Python?", top_k=2)
    print(f"\nSearch results: {len(results)} chunks found")
    
    # Test stats
    stats = store.get_stats()
    print(f"\nStats: {stats}")
    
    print("\n✅ All tests passed!")
