"""
Vector Store for RAG System
============================
Manages document embeddings and similarity search using ChromaDB
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from pathlib import Path


class VectorStore:
    """Manages vector embeddings and similarity search"""
    
    def __init__(self, persist_directory: str = "data/chroma_db"):
        """
        Initialize ChromaDB vector store
        
        Args:
            persist_directory: Directory to store embeddings
        """
        # Create persist directory
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection for documents
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"description": "PDF document chunks for RAG"}
        )
        
        print(f"✅ Vector store initialized at {persist_directory}")
    
    def add_document(self, doc_id: int, chunks: List[Dict], metadata: Dict):
        """
        Add document chunks to vector store
        
        Args:
            doc_id: Document ID from database
            chunks: List of text chunks
            metadata: Document metadata (filename, etc.)
        """
        try:
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for chunk in chunks:
                documents.append(chunk['text'])
                metadatas.append({
                    'doc_id': doc_id,
                    'chunk_id': chunk['id'],
                    'filename': metadata.get('filename', 'unknown'),
                    'start_char': chunk['start_char'],
                    'end_char': chunk['end_char']
                })
                ids.append(f"doc_{doc_id}_chunk_{chunk['id']}")
            
            # Add to collection
            # ChromaDB will automatically generate embeddings
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
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
            # Build where filter if doc_id specified
            where_filter = None
            if doc_id is not None:
                where_filter = {"doc_id": doc_id}
            
            # Perform similarity search
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=where_filter
            )
            
            # Format results
            chunks = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    chunks.append({
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    })
            
            print(f"✅ Found {len(chunks)} relevant chunks")
            return chunks
            
        except Exception as e:
            print(f"❌ Error searching vector store: {str(e)}")
            return []
    
    def delete_document(self, doc_id: int):
        """
        Delete all chunks from a document
        
        Args:
            doc_id: Document ID to delete
        """
        try:
            # Get all IDs for this document
            results = self.collection.get(
                where={"doc_id": doc_id}
            )
            
            if results and results['ids']:
                self.collection.delete(ids=results['ids'])
                print(f"✅ Deleted document {doc_id} from vector store")
            else:
                print(f"⚠️ No chunks found for document {doc_id}")
                
        except Exception as e:
            print(f"❌ Error deleting document: {str(e)}")
            raise
    
    def count_documents(self) -> int:
        """Get total number of chunks in the store"""
        try:
            return self.collection.count()
        except:
            return 0
    
    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        return {
            'total_chunks': self.count_documents(),
            'collection_name': self.collection.name
        }


# Test the vector store if run directly
if __name__ == "__main__":
    print("Testing Vector Store...")
    
    store = VectorStore("data/test_chroma_db")
    
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
