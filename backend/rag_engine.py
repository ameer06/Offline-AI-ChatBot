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
    
    def retrieve_context_from_docs(self, query: str, doc_ids: list, top_k: int = 3) -> List[Dict]:
        """
        Retrieve relevant context from specific documents only
        
        Args:
            query: User's question
            doc_ids: List of document IDs to search
            top_k: Number of relevant chunks to retrieve per document
            
        Returns:
            List of relevant text chunks from selected documents
        """
        print(f"🔍 retrieve_context_from_docs called with doc_ids: {doc_ids}")
        all_results = []
        
        # Search each selected document
        for doc_id in doc_ids:
            print(f"   Searching vector store for doc_id: {doc_id}")
            results = self.vector_store.search(query, top_k=top_k, doc_id=doc_id)
            print(f"   Found {len(results)} chunks for doc_id {doc_id}")
            if results:
                print(f"   Metadata of first result: {results[0].get('metadata')}")
            all_results.extend(results)
        
        # Sort all results by similarity and return top_k overall
        all_results.sort(key=lambda x: x.get('distance', 1.0))
        print(f"✅ Total {len(all_results)} chunks collected, returning top {top_k}")
        return all_results[:top_k]
    
    def build_prompt_with_context(self, query: str, context_chunks: List[Dict], conversation_history: list = None) -> str:
        """
        Build a prompt that includes retrieved context and conversation history
        
        Args:
            query: User's question
            context_chunks: Retrieved relevant chunks
            conversation_history: Previous messages for context
            
        Returns:
            Enhanced prompt with context
        """
        if conversation_history is None:
            conversation_history = []
            
        if not context_chunks:
            return self.build_prompt_with_history(query, conversation_history)
        
        # Build context section
        context_text = "\n\n".join([
            f"[Document: {chunk['metadata'].get('filename', 'Unknown')}]\n{chunk['text']}"
            for chunk in context_chunks
        ])  
        
        # Build conversation history
        history_text = ""
        if conversation_history:
            history_text = "\n\nPrevious conversation:\n"
            for msg in conversation_history:
                role = "User" if msg['role'] == 'user' else "Assistant"
                history_text += f"{role}: {msg['content']}\n"
        
        # Improved prompt that handles both casual chat and questions
        prompt = f"""You are a helpful AI assistant. Your name is "Offline AI Chatbot with RAG". You are an offline, privacy-focused conversational AI system with document understanding capabilities.

IDENTITY GUIDELINES:
- Only mention your name or introduce yourself when specifically asked about your identity, name, or who you are
- For all other questions, just answer naturally without mentioning your name or capabilities
- You run completely offline using Ollama for privacy and security

CONVERSATION GUIDELINES:
1. If the user's message is a casual response (like "cool", "okay", "thanks", "hi", etc.), just respond naturally and conversationally. DON'T mention the documents.
2. If the user asks a real question about the documents, use the context below to answer accurately.
3. If the question is NOT related to the documents, just answer normally based on your general knowledge.
4. Be friendly and natural in your responses.
{history_text}
Document Context (use ONLY if the question relates to this):
{context_text}

User's current message: {query}

Your response:"""
        
        return prompt
    
    def build_prompt_with_history(self, query: str, conversation_history: list) -> str:
        """
        Build a prompt with conversation history but no document context
        
        Args:
            query: User's question
            conversation_history: Previous messages for context
            
        Returns:
            Prompt with conversation history
        """
        # Build conversation history
        history_text = ""
        if conversation_history:
            history_text = "\n\nPrevious conversation:\n"
            for msg in conversation_history:
                role = "User" if msg['role'] == 'user' else "Assistant"
                history_text += f"{role}: {msg['content']}\n"
        
        prompt = f"""You are a helpful AI assistant. Your name is "Offline AI Chatbot with RAG". You are an offline, privacy-focused conversational AI system.

IDENTITY GUIDELINES:
- Only mention your name or introduce yourself when specifically asked about your identity, name, or who you are
- For all other questions, just answer naturally without mentioning your name
- You run completely offline using Ollama for privacy and security
{history_text}
User's current message: {query}

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
    
    def chat_with_rag(self, query: str, model: str = "llama3.2", use_rag: bool = True, top_k: int = 3, conversation_history: list = None, selected_doc_ids: list = None) -> Dict:
        """
        Complete RAG pipeline: retrieve context and generate response
        
        Args:
            query: User's question
            model: AI model to use
            use_rag: Whether to use RAG (retrieve context)
            top_k: Number of context chunks to retrieve
            conversation_history: List of previous messages for context
            selected_doc_ids: List of document IDs to search (None = search all)
            
        Returns:
            Dictionary with response and metadata
        """
        if conversation_history is None:
            conversation_history = []
        
        if selected_doc_ids is None:
            selected_doc_ids = []
            
        context_chunks = []
        
        # Retrieve context if RAG is enabled and documents exist
        if use_rag and self.vector_store.count_documents() > 0:
            # If specific documents are selected, search only those
            if selected_doc_ids:
                print(f"🎯 Searching only selected documents: {selected_doc_ids}")
                context_chunks = self.retrieve_context_from_docs(query, selected_doc_ids, top_k=top_k)
            else:
                print("📚 No documents selected, searching all documents")
                context_chunks = self.retrieve_context(query, top_k=top_k)
        
        # Build prompt with or without context
        if context_chunks:
            prompt = self.build_prompt_with_context(query, context_chunks, conversation_history)
            has_context = True
        else:
            # No document context, but still include conversation history
            prompt = self.build_prompt_with_history(query, conversation_history)
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
