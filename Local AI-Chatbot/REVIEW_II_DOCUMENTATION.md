LexaMind — Offline AI Chatbot with RAG

Project Review II — Development Progress Report

Project Title: LexaMind — Offline AI Chatbot with RAG
Review Date: 09 March 2026
Total Marks: 15



1. IMPLEMENTATION PROGRESS (50–70%)


1.1 System Architecture

LexaMind follows a three-tier client-server architecture designed for fully offline operation.

    Presentation Tier (Frontend — HTML/CSS/JavaScript + Electron Shell)
            |
            | HTTP REST API
            |
    Application Tier (Flask Backend — RAG Engine, Vector Store, PDF Processor)
            |
            |
    Data Tier (SQLite + Vector Store on Disk)       Ollama LLM (llama3.2)


1.2 Technology Stack

    Layer                 Technology                         Purpose
    Backend Framework     Python 3.8+, Flask                 REST API server
    AI Engine             Ollama (Llama 3.2)                 Local LLM inference
    Database              SQLite                             Chat history and doc metadata
    Vector Store          Custom (NumPy + Cosine Similarity) Semantic document search
    PDF Processing        PyPDF2                             Text extraction from PDFs
    Frontend              HTML5, CSS3, Vanilla JavaScript    User interface
    Desktop App           Electron.js                        Cross-platform packaging
    API Libraries         Flask-CORS, Requests               Cross-origin and HTTP calls


1.3 Module Breakdown

    No.   Module              File                         Lines    Status
    1     Flask API Server    backend/app.py               826      Complete
    2     Database Manager    backend/database.py          464      Complete
    3     RAG Engine          backend/rag_engine.py        245      Complete
    4     Vector Store        backend/vector_store.py      250      Complete
    5     PDF Processor       backend/pdf_processor.py     134      Complete
    6     Frontend UI         frontend/index.html          2,193    Complete
    7     Electron Main       electron/main.js             143      Complete
    8     Electron Preload    electron/preload.js          17       Complete
          Total               8 files                      ~4,272


1.4 API Endpoints Implemented (27 Total)

    Core Chat
    POST   /chat                              Send message and get AI response (with RAG)
    GET    /health                            Server health check
    GET    /                                  API info page

    Model Management
    GET      /models                          List available Ollama models
    GET/POST /active-model                    Get or set the active model
    POST     /download-model                  Download a new model

    Conversation Management
    POST   /conversations/new                 Create new conversation
    GET    /conversations                     List all conversations
    GET    /conversations/<id>                Get conversation with messages
    DELETE /conversations/<id>                Delete a conversation
    POST   /conversations/<id>/activate       Set active conversation

    Document Management
    POST   /upload                            Upload and process a PDF
    GET    /documents                         List all uploaded documents
    DELETE /documents/<id>                    Delete a document

    Study Assistant
    POST   /documents/<id>/regenerate-summary Generate AI summary of document
    POST   /documents/<id>/quiz               Generate 5 MCQ questions
    POST   /documents/<id>/flashcards         Generate 8 flashcard pairs


1.5 Features Implemented

    No.   Feature                       Description
    1     AI Chat                       Real-time AI with markdown and code rendering
    2     Multi-Conversation            Create, switch, delete, auto-title conversations
    3     Model Switching               Dropdown to switch between installed Ollama models
    4     PDF Upload and Processing     Upload, extract text, chunk, and vectorize
    5     RAG-Enhanced Chat             Toggle for document-context-aware responses
    6     Selective Document Query      Checkbox to restrict RAG to specific documents
    7     Study Assistant — Summary     AI-generated document summaries
    8     Study Assistant — Quiz        Auto-generated MCQ from document content
    9     Study Assistant — Flashcards  Auto-generated flashcard pairs
    10    Dark Mode UI                  Modern ChatGPT-inspired interface
    11    Responsive Design             Mobile-compatible with hamburger sidebar
    12    Desktop App                   Electron packaging with custom controls
    13    Chat History Persistence      SQLite-backed storage across sessions
    14    Offline Operation             Fully functional without internet after setup


1.6 Estimated Completion: ~65–70%

    Completed:
    - Core chat engine with RAG pipeline
    - Full database integration with 3 tables
    - Document management (upload, process, delete)
    - Study Assistant tools (summary, quiz, flashcards)
    - Responsive frontend with dark mode
    - Desktop packaging with Electron

    Remaining (~30–35%):
    - Advanced prompt engineering and fine-tuning
    - Multi-format document support (DOCX, TXT, images)
    - User authentication and multi-user support
    - Export chat history feature
    - Installer packaging for distribution



2. DATABASE DESIGN AND INTEGRATION


2.1 Database Engine

    SQLite was selected for:
    - Zero-configuration setup (no separate server process)
    - Ideal fit for offline, single-user desktop applications
    - File-based storage (data/chatbot.db)
    - Cross-platform compatibility


2.2 Entity-Relationship Diagram

    conversations                          messages
    +-------------------------+            +------------------------------+
    | PK  id         INTEGER  |----+       | PK  id              INTEGER |
    |     title      TEXT     |    |       | FK  conversation_id INTEGER |
    |     created_at TIMESTAMP|    +------>|     role            TEXT     |
    |     updated_at TIMESTAMP|            |     content         TEXT     |
    |     model_used TEXT     |            |     timestamp       TIMESTAMP|
    +-------------------------+            |     has_rag_context BOOLEAN  |
                                           +------------------------------+

    documents
    +-----------------------------+
    | PK  id          INTEGER     |
    |     filename    TEXT        |
    |     file_path   TEXT        |
    |     upload_date TIMESTAMP   |
    |     file_size   INTEGER     |
    |     page_count  INTEGER     |
    |     status      TEXT        |
    |     summary     TEXT        |
    +-----------------------------+


2.3 Table Schemas

    Table: conversations

    Column       Type        Constraints
    id           INTEGER     PRIMARY KEY, AUTOINCREMENT
    title        TEXT        NOT NULL
    created_at   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
    updated_at   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
    model_used   TEXT        DEFAULT 'llama3.2'

    Table: messages

    Column            Type        Constraints
    id                INTEGER     PRIMARY KEY, AUTOINCREMENT
    conversation_id   INTEGER     NOT NULL, FK -> conversations(id) ON DELETE CASCADE
    role              TEXT        NOT NULL, CHECK(role IN ('user', 'assistant'))
    content           TEXT        NOT NULL
    timestamp         TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
    has_rag_context   BOOLEAN     DEFAULT 0

    Table: documents

    Column        Type        Constraints
    id            INTEGER     PRIMARY KEY, AUTOINCREMENT
    filename      TEXT        NOT NULL
    file_path     TEXT        NOT NULL
    upload_date   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
    file_size     INTEGER
    page_count    INTEGER
    status        TEXT        DEFAULT 'processing', CHECK IN ('processing','ready','error')
    summary       TEXT        DEFAULT NULL


2.4 Indexes

    Index Name                    Table           Column(s)          Purpose
    idx_messages_conversation     messages        conversation_id    Fast message lookup by conversation
    idx_conversations_updated     conversations   updated_at DESC    Efficient ordered conversation list


2.5 Relationships and Constraints

    - One-to-Many: One conversation contains many messages
    - Cascade Delete: Deleting a conversation automatically removes all associated messages
    - CHECK Constraints: role restricted to 'user'/'assistant'; status restricted to 'processing'/'ready'/'error'
    - Schema Migration: Automatic column addition (summary) for backward compatibility


2.6 Vector Store (Supplementary Storage)

    In addition to SQLite, a pickle-based vector store (data/vector_db/) persists document embeddings:
    - Stores term-frequency vector representations of document chunks
    - Enables cosine similarity search for RAG retrieval
    - Separate from SQLite by design — optimized for numerical array operations
    - Supports per-document indexing and deletion


2.7 Database Integration Points

    Operation              Database Interaction
    User sends message     Save user message, get AI response, save assistant message
    New conversation       INSERT into conversations, return ID
    Load conversation      SELECT conversation + JOIN messages, ordered by timestamp
    Upload PDF             INSERT document metadata, update status after processing
    Generate summary       Call LLM, store result in documents.summary column
    Delete conversation    CASCADE delete removes conversation and all messages
    App startup            Auto-create tables if not exist, run schema migrations



3. WORKING MODULES DEMONSTRATION


3.1 Module: AI Chat Engine

    Purpose: Core conversational AI functionality

    Process:
    1. User types a message in the frontend
    2. Frontend sends POST request to /chat endpoint
    3. Backend sends prompt to Ollama's local LLM API
    4. LLM generates a response
    5. Both user message and AI response are saved to the database
    6. Response is rendered with markdown formatting and code syntax highlighting

    Key capabilities: Real-time responses, markdown rendering, code block highlighting, conversation context awareness


3.2 Module: RAG Pipeline (Retrieval Augmented Generation)

    Purpose: Enable the AI to answer questions based on uploaded documents

    Pipeline:
    PDF Upload -> Text Extraction -> Text Chunking -> Vectorization -> Storage
                                                                         |
    User Query -> Vectorize Query -> Cosine Similarity Search -----------+
                                            |
                               Top-K Relevant Chunks
                                            |
                               Build Augmented Prompt (Query + Context + History)
                                            |
                               Send to Ollama LLM
                                            |
                               Context-Aware Response

    Technical details:
    - Chunk size: 512 characters with 50-character overlap
    - Vectorization: Term-frequency based approach
    - Similarity metric: Cosine similarity
    - Default retrieval: Top 3 most relevant chunks
    - Selective querying: Users can select specific documents to restrict search scope


3.3 Module: Document Management

    Purpose: Upload, process, store, and manage PDF documents

    Capabilities:
    - Upload PDF files (maximum 10 MB)
    - Automatic text extraction using PyPDF2
    - Text chunking with configurable size and overlap
    - Document status tracking (processing, ready, error)
    - Document deletion (removes from database, vector store, and filesystem)
    - Document listing with metadata (filename, size, pages, status)


3.4 Module: Study Assistant

    Purpose: AI-powered learning tools generated from uploaded documents

    Tool          Description                                   Output
    Summary       Generates a concise 3-line document summary   Text summary in document card
    Quiz          Creates 5 MCQ questions from document content  Interactive quiz with 4 options
    Flashcards    Generates 8 question-answer pairs             Interactive flip cards for study


3.5 Module: Conversation Management

    Purpose: Manage multiple chat sessions with persistence

    Features:
    - Create new conversations
    - Auto-generate conversation titles from first user message
    - Switch between conversations with full history loading
    - Delete conversations with cascade message deletion
    - Conversation list sorted by most recent activity


3.6 Module: Model Management

    Purpose: Switch between different Ollama AI models

    Features:
    - List all locally installed models
    - Switch active model via dropdown selector
    - Download new models from within the application
    - Each conversation records which model was used


3.7 Module: Frontend UI

    Purpose: Modern, responsive user interface

    Design: ChatGPT-inspired dark mode with purple accent theme
    Layout:
    - Sidebar: Conversation list and document list with upload button
    - Main area: Chat messages with input field
    - Header: Model selector and RAG toggle
    - Responsive: Hamburger menu on mobile and tablet screens


3.8 Module: Desktop Application (Electron)

    Purpose: Package the web application as a standalone desktop program

    Features:
    - Custom frameless window with minimize, maximize, and close controls
    - Auto-launches Flask backend server on application startup
    - Loads frontend in Electron BrowserWindow
    - Cross-platform support (Windows, macOS, Linux)



4. DOCUMENTATION UPDATE


4.1 Project Documentation Files

    No.   Document                     Description                          Status
    1     README.md                    Installation and usage guide         Updated
    2     ABSTRACT.md                  Academic abstract                    Updated
    3     PROJECT_SUBMISSION.md        Formal abstract with keywords        Updated
    4     HOW_IT_WORKS.md              Technical architecture explanation   Updated
    5     PROJECT_FAQ.md               Frequently asked questions           Updated
    6     CUSTOMIZATION.md             Customization guide                  Available
    7     SYSTEM_REQUIREMENTS.md       Hardware and software requirements   Available
    8     QUICKSTART.md                Quick setup guide                    Available
    9     README_DESKTOP.md            Desktop application documentation    Available
    10    REVIEW_II_DOCUMENTATION.md   This document                        New


4.2 Code Documentation

    - All Python modules include module-level docstrings describing their purpose
    - All classes include class-level docstrings
    - All functions include docstrings with Args and Returns documentation
    - Database queries are commented inline for clarity
    - Frontend JavaScript functions include purpose descriptions in comments


4.3 Project Structure

    LexaMind/
        backend/
            app.py              Flask API server (27 endpoints)
            database.py         SQLite database manager
            rag_engine.py       RAG pipeline orchestrator
            vector_store.py     Cosine similarity vector search
            pdf_processor.py    PDF text extraction and chunking
            requirements.txt    Python dependencies
        frontend/
            index.html          Complete UI (HTML, CSS, JavaScript)
        electron/
            main.js             Electron main process
            preload.js          Electron preload script
        data/
            chatbot.db          SQLite database file
            uploads/            Uploaded PDF storage
        README.md
        ABSTRACT.md
        PROJECT_SUBMISSION.md
        HOW_IT_WORKS.md
        PROJECT_FAQ.md
        CUSTOMIZATION.md
        SYSTEM_REQUIREMENTS.md
        QUICKSTART.md
        README_DESKTOP.md
        REVIEW_II_DOCUMENTATION.md
        package.json            Node.js dependencies for Electron
        install.bat             Windows installer script
        launch_chatbot.bat      Launch script
        start_all.bat           Start backend and frontend



Prepared for Project Review II
LexaMind — Offline AI Chatbot with RAG
