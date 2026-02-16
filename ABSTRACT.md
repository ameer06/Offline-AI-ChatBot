# Abstract

## Offline AI Chatbot with RAG: An Offline Approach to Context-Aware Conversational AI

**Author**: [Your Name]  
**Institution**: [Your University Name]  
**Department**: [Your Department]  
**Academic Year**: 2024-2025

---

### Abstract

The proliferation of cloud-based conversational AI systems has raised concerns regarding data privacy, internet dependency, and accessibility in resource-constrained environments. This project presents a fully offline Offline AI Chatbot system that leverages Retrieval Augmented Generation (RAG) to provide context-aware responses while maintaining complete data sovereignty. The system architecture combines a locally-hosted large language model (LLM) through Ollama with a vector database implementation using ChromaDB for semantic document retrieval.

The proposed solution addresses the fundamental limitation of traditional LLMs—their static knowledge base—by implementing a dynamic RAG pipeline that retrieves relevant information from user-uploaded PDF documents. When a query is received, the system performs semantic search across vectorized document chunks and augments the LLM prompt with contextually relevant information, enabling the model to generate accurate responses based on current or domain-specific knowledge not present in its training data.

The system employs a client-server architecture with a Flask-based REST API backend and a responsive web-based frontend. Document processing utilizes PyPDF2 for text extraction and implements a chunking strategy with overlapping segments to preserve contextual continuity. Text chunks are converted to high-dimensional vector embeddings using sentence transformers, enabling efficient similarity-based retrieval. Chat history persistence is achieved through SQLite database integration, allowing conversation continuity across sessions.

Key technical contributions include: (1) a modular RAG pipeline that seamlessly integrates document retrieval with prompt engineering, (2) an intuitive user interface with real-time document management and conversation tracking, (3) complete offline functionality eliminating external API dependencies, and (4) a scalable vector storage mechanism supporting multiple concurrent document sources with selective retrieval.

Performance evaluation demonstrates response generation times of 2-10 seconds depending on hardware specifications, with negligible latency for document retrieval operations. The system successfully processes multi-page PDF documents and maintains conversation context across extended dialogue sessions. User interface enhancements including dark mode support, dynamic animations, and responsive design contribute to improved user experience.

This implementation demonstrates the viability of deploying sophisticated conversational AI capabilities in offline environments, with applications in educational institutions, healthcare facilities, legal document review, and scenarios requiring data confidentiality. Future work includes optimization of embedding model selection, implementation of multi-modal document support, and enhancement of prompt engineering techniques for improved factual accuracy.

---

### Keywords

Conversational AI, Retrieval Augmented Generation, Offline Systems, Large Language Models, Vector Databases, Document Processing, Natural Language Processing, Semantic Search, Privacy-Preserving AI

---

### Project Classification

- **Domain**: Artificial Intelligence, Natural Language Processing
- **Type**: Full-Stack Application Development
- **Technologies**: Python, Flask, JavaScript, ChromaDB, Ollama, SQLite
- **Category**: Final Year Project
