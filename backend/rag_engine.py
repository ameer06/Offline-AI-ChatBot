"""
RAG Engine  
==========
Orchestrates Retrieval Augmented Generation
"""

import requests
from typing import List, Dict, Optional
from vector_store import VectorStore


class RAGEngine:
    """Manages the RAG pipeline for context-aware responses"""
    
    def __init__(self, vector_store: VectorStore, ollama_url: str = "http://localhost:11434/api/generate"):
        """
        Initialize RAG engine
        
        Args:
            vector_store: Vector store instance
            ollama_url: Ollama API endpoint
        """
        self.vector_store = vector_store
        self.ollama_url = ollama_url
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve relevant context for a query
        
        Args:
            query: User's question
            top_k: Number of relevant chunks to retrieve
            
        Returns:
            List of relevant text chunks
        """
        return self.vector_store.search(query, top_k=top_k)
    
    def build_prompt_with_context(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Build a prompt that includes retrieved context
        
        Args:
            query: User's question
            context_chunks: Retrieved relevant chunks
            
        Returns:
            Enhanced prompt with context
        """
        if not context_chunks:
            return query
        
        # Build context section
        context_text = "\n\n".join([
            f"[Document: {chunk['metadata'].get('filename', 'Unknown')}]\n{chunk['text']}"
            for chunk in context_chunks
        ])  
        
        # Improved prompt that handles both casual chat and questions
        prompt = f"""You are a helpful AI assistant. You have access to some document content below.

IMPORTANT INSTRUCTIONS:
1. If the user's message is a casual response (like "cool", "okay", "thanks", "hi", etc.), just respond naturally and conversationally. DON'T mention the documents.
2. If the user asks a real question about the documents, use the context below to answer accurately.
3. If the question is NOT related to the documents, just answer normally based on your general knowledge.
4. Be friendly and natural in your responses.

Document Context (use ONLY if the question relates to this):
{context_text}

User's message: {query}

Your response:"""
        
        return prompt
    
    def generate_response(self, prompt: str, model: str = "llama3.2", timeout: int = 120) -> str:
        """
        Generate AI response using Ollama
        
        Args:
            prompt: The prompt (with or without context)
            model: AI model to use
            timeout: Request timeout in seconds
            
        Returns:
            AI-generated response
        """
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'Sorry, I could not generate a response.')
            else:
                return f"Error: Ollama returned status code {response.status_code}"
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat_with_rag(self, query: str, model: str = "llama3.2", use_rag: bool = True, top_k: int = 3) -> Dict:
        """
        Complete RAG pipeline: retrieve context and generate response
        
        Args:
            query: User's question
            model: AI model to use
            use_rag: Whether to use RAG (retrieve context)
            top_k: Number of context chunks to retrieve
            
        Returns:
            Dictionary with response and metadata
        """
        context_chunks = []
        
        # Retrieve context if RAG is enabled and documents exist
        if use_rag and self.vector_store.count_documents() > 0:
            context_chunks = self.retrieve_context(query, top_k=top_k)
        
        # Build prompt with or without context
        if context_chunks:
            prompt = self.build_prompt_with_context(query, context_chunks)
            has_context = True
        else:
            prompt = query
            has_context = False
        
        # Generate response
        response = self.generate_response(prompt, model=model)
        
        return {
            'response': response,
            'has_rag_context': has_context,
            'context_chunks_used': len(context_chunks),
            'sources': [chunk['metadata'].get('filename') for chunk in context_chunks] if context_chunks else []
        }


# Test if run directly
if __name__ == "__main__":
    print("RAG Engine initialized")
    print("Ready to handle context-aware queries!")
