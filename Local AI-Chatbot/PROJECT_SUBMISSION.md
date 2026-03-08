Final Year Project Submission

Project Title: LexaMind — Offline AI Chatbot with RAG

---

Abstract

In the era of increasing privacy concerns and dependency on cloud-based AI services, this project presents the development of a locally-hosted AI chatbot that leverages open-source Large Language Models (LLMs) to provide intelligent conversational capabilities without relying on external APIs or internet connectivity. The system addresses critical challenges such as data privacy, operational costs, and service availability by implementing a complete end-to-end solution that runs entirely on the user's local machine.

The chatbot is built using a modern web-based architecture consisting of a Flask backend server that interfaces with Ollama, a lightweight framework for running LLMs locally, and an interactive HTML/JavaScript frontend that provides an intuitive user interface. The system utilizes the Llama 3.2 model, a state-of-the-art open-source language model, to generate human-like responses to user queries. A Retrieval Augmented Generation (RAG) pipeline enables the chatbot to answer questions based on user-uploaded PDF documents by performing semantic search across vectorized document chunks.

Key features of the implementation include:
- Complete Privacy: All data processing occurs locally with no external data transmission
- Zero API Costs: Elimination of subscription fees and per-request charges
- Offline Capability: Full functionality without internet connectivity after initial setup
- RAG Integration: Document-based question answering using semantic retrieval
- Study Assistant: AI-generated summaries, quizzes, and flashcards from uploaded documents
- Cross-Platform Compatibility: Runs on Windows, macOS, and Linux systems
- Customizable AI Models: Support for multiple LLM variants based on computational requirements

The technical stack comprises Python-Flask for the RESTful API backend, SQLite for persistent data storage, a custom vector store with cosine similarity for semantic search, PyPDF2 for document processing, and a responsive web interface built with HTML5, CSS3, and vanilla JavaScript. The system also includes an Electron wrapper for cross-platform desktop application distribution. The architecture follows a client-server model where the frontend communicates via HTTP requests to the Flask backend, which orchestrates interactions between the database, RAG engine, and Ollama inference service.

Performance evaluation demonstrates that the chatbot achieves response times of 2-10 seconds depending on hardware specifications while maintaining complete data sovereignty. The modular architecture allows for easy customization of AI models, user interfaces, and system prompts, making it adaptable for various use cases including educational assistants, coding helpers, and general-purpose conversational agents.

This project demonstrates the feasibility and advantages of deploying AI-powered applications locally, offering a viable alternative to cloud-dependent solutions for users and organizations prioritizing data privacy and operational independence.

---

Keywords

Artificial Intelligence, Large Language Models, Retrieval Augmented Generation, Ollama, Flask, Privacy-Preserving AI, Local Machine Learning, Chatbot Development, Open-Source LLM, Natural Language Processing, Semantic Search, Web Application Development

---

Technology Stack Summary

Backend:
- Python 3.8+
- Flask (Web Framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- SQLite (Database)
- Ollama (LLM Inference)
- PyPDF2 (PDF Processing)
- NumPy (Vector Operations)

Frontend:
- HTML5
- CSS3 (Responsive Design with Dark Mode)
- JavaScript (Vanilla)
- Marked.js (Markdown Rendering)
- Highlight.js (Code Syntax Highlighting)

AI Model:
- Llama 3.2 (default, ~2 GB)
- Supports: Mistral, CodeLlama, Gemma variants

Desktop Application:
- Electron.js (Cross-Platform Packaging)
- Node.js

Deployment:
- Local hosting on Windows/macOS/Linux
- No cloud infrastructure required
