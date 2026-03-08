How the Project Works

LexaMind — Offline AI Chatbot with RAG

---

Overview

LexaMind is a fully offline AI-powered chatbot that uses Retrieval Augmented Generation (RAG) to answer questions based on uploaded PDF documents, while also functioning as a general-purpose conversational assistant with study tools.

---

Architecture

  +-----------------------------------------------------------+
  |                       FRONTEND                             |
  |  (HTML/CSS/JavaScript — index.html)                        |
  |  - User Interface                                          |
  |  - Chat Display with Markdown Rendering                    |
  |  - Document Management                                     |
  |  - Study Assistant (Summary, Quiz, Flashcards)             |
  +----------------------------+------------------------------+
                               | HTTP Requests (Port 5000)
                               v
  +-----------------------------------------------------------+
  |                       BACKEND                              |
  |  (Python Flask — app.py)                                   |
  |  - REST API Endpoints (27 total)                           |
  |  - Request Routing and Business Logic                      |
  +--------+-----------+------------+-------------------------+
           |           |            |
           v           v            v
  +-----------+  +----------+  +--------------+
  | Database  |  |   RAG    |  |   Ollama     |
  | (SQLite)  |  |  Engine  |  |  (AI Model)  |
  +-----------+  +----------+  +--------------+
                      |
                      v
               +--------------+
               | Vector Store |
               | (TF-Cosine)  |
               +--------------+
                      |
                      v
               +--------------+
               |PDF Processor |
               +--------------+

---

Component Breakdown

1. Frontend (frontend/index.html)

Purpose: User interface for all interactions

Key Features:
- Chat interface with markdown and code syntax rendering
- PDF upload and document management in sidebar
- Conversation history with create, switch, and delete
- Model selection dropdown
- RAG toggle for document-based Q&A
- Study Assistant buttons (Summary, Quiz, Flashcards)
- Responsive design with dark mode

Technologies:
- HTML5, CSS3 (with animations), Vanilla JavaScript
- Marked.js (markdown rendering)
- Highlight.js (code syntax highlighting)

---

2. Backend API (backend/app.py)

Purpose: Handles all server-side logic and routing

Main Endpoints:

| Endpoint                          | Method | Purpose                           |
|-----------------------------------|--------|-----------------------------------|
| /chat                             | POST   | Send message, get AI response     |
| /health                           | GET    | Server health check               |
| /models                           | GET    | List available AI models          |
| /active-model                     | GET/POST | Get or set active model         |
| /download-model                   | POST   | Download new model                |
| /conversations/new                | POST   | Create new conversation           |
| /conversations                    | GET    | List all conversations            |
| /conversations/<id>               | GET    | Get conversation with messages    |
| /conversations/<id>               | DELETE | Delete a conversation             |
| /conversations/<id>/activate      | POST   | Set active conversation           |
| /upload                           | POST   | Upload and process PDF            |
| /documents                        | GET    | List all documents                |
| /documents/<id>                   | DELETE | Delete a document                 |
| /documents/<id>/regenerate-summary| POST   | Generate document summary         |
| /documents/<id>/quiz              | POST   | Generate quiz from document       |
| /documents/<id>/flashcards        | POST   | Generate flashcards from document |

Technologies:
- Flask (web framework)
- Flask-CORS (cross-origin requests)
- Requests (HTTP calls to Ollama)

---

3. Database (backend/database.py)

Purpose: Persistent storage for chat history and document metadata

Tables:

Conversations Table:
- id (PRIMARY KEY, AUTOINCREMENT)
- title (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- model_used (TEXT)

Messages Table:
- id (PRIMARY KEY, AUTOINCREMENT)
- conversation_id (FOREIGN KEY -> conversations.id, ON DELETE CASCADE)
- role (TEXT, CHECK: 'user' or 'assistant')
- content (TEXT)
- timestamp (TIMESTAMP)
- has_rag_context (BOOLEAN)

Documents Table:
- id (PRIMARY KEY, AUTOINCREMENT)
- filename (TEXT)
- file_path (TEXT)
- upload_date (TIMESTAMP)
- file_size (INTEGER)
- page_count (INTEGER)
- status (TEXT, CHECK: 'processing', 'ready', 'error')
- summary (TEXT)

Storage: SQLite database (data/chatbot.db)

---

4. RAG Engine (backend/rag_engine.py)

Purpose: Retrieval Augmented Generation pipeline

Workflow:

  User Query
      |
  1. Retrieve Context (search vector store for relevant chunks)
      |
  2. Build Enhanced Prompt (query + context + conversation history)
      |
  3. Generate Response (send augmented prompt to Ollama)
      |
  Context-Aware AI Response

Key Methods:
- retrieve_context() — Find relevant PDF chunks globally
- retrieve_context_from_docs() — Find chunks from selected documents only
- build_prompt_with_context() — Create enhanced prompt with RAG context
- build_prompt_with_history() — Create prompt with conversation history only
- generate_response() — Get AI response from Ollama
- chat_with_rag() — Complete RAG pipeline

---

5. Vector Store (backend/vector_store.py)

Purpose: Store and search document embeddings for semantic retrieval

How It Works:
1. PDF text is split into chunks (512 characters with 50-character overlap)
2. Each chunk is vectorized using term-frequency representation
3. Vectors are stored in memory with disk persistence (pickle format)
4. User query is vectorized and compared using cosine similarity
5. Top-K most relevant chunks are returned to the RAG engine

Storage: data/vector_db/ (pickle-based persistence)

Technology: NumPy + custom cosine similarity implementation

---

6. PDF Processor (backend/pdf_processor.py)

Purpose: Extract and chunk PDF text for the RAG pipeline

Process:
1. PDF uploaded and saved to data/uploads/
2. Text extracted page-by-page using PyPDF2
3. Text split into overlapping chunks (512 chars, 50-char overlap)
4. Chunks returned with metadata (position, length)

Input: PDF file
Output: List of text chunks with metadata

---

7. Ollama Integration

Purpose: Run AI models locally without internet

How It Works:
- Ollama runs as a background service on port 11434
- Backend sends HTTP POST requests to Ollama's API
- Ollama processes prompts using the selected LLM
- Fully offline operation — no internet required

API Call Format:
  POST http://localhost:11434/api/generate
  {
    "model": "llama3.2",
    "prompt": "User question here",
    "stream": false
  }

---

Data Flow

Scenario 1: Normal Chat (No RAG)

  User types message
  -> Frontend sends POST to /chat
  -> Backend forwards prompt to Ollama
  -> Ollama generates response
  -> Backend saves message pair to database
  -> Response sent to frontend
  -> Displayed in chat

Scenario 2: RAG-Enhanced Chat

  User types question (with documents uploaded and selected)
  -> Frontend sends POST to /chat with use_rag=true and selected doc IDs
  -> Backend invokes RAG Engine
  -> RAG Engine searches vector store for relevant chunks
  -> RAG Engine builds enhanced prompt with context
  -> Enhanced prompt sent to Ollama
  -> Ollama generates context-aware response
  -> Response and metadata saved to database
  -> Response displayed with RAG badge indicator

Scenario 3: PDF Upload

  User selects PDF file
  -> Frontend sends file to /upload
  -> Backend saves PDF to data/uploads/
  -> PDF Processor extracts text
  -> Text chunked into overlapping segments
  -> Chunks vectorized and stored in vector store
  -> Document metadata saved to database
  -> Document appears in sidebar with status

Scenario 4: Study Assistant

  User clicks Summary/Quiz/Flashcards on a document
  -> Backend retrieves top text chunks for the document
  -> LLM generates study content from the chunks
  -> Results returned and displayed in the UI

---

Key Technologies

| Component     | Technology               | Purpose                    |
|---------------|--------------------------|----------------------------|
| Frontend      | HTML/CSS/JavaScript      | User interface             |
| Backend       | Flask (Python)           | REST API server            |
| Database      | SQLite                   | Chat history and metadata  |
| Vector Store  | NumPy + Cosine Similarity| Semantic document search   |
| AI Model      | Ollama (llama3.2)        | Local text generation      |
| PDF Parser    | PyPDF2                   | Text extraction            |
| Markdown      | Marked.js                | Rich text rendering        |
| Syntax        | Highlight.js             | Code block highlighting    |
| Desktop App   | Electron                 | Cross-platform packaging   |

---

Storage Locations

  LexaMind/
  |-- backend/
  |   |-- data/
  |   |   |-- chatbot.db          (SQLite database)
  |   |   |-- uploads/            (Uploaded PDFs)
  |   |   |-- vector_db/          (Vector embeddings)
  |   |-- app.py                  (Main backend server)
  |   |-- database.py             (Database operations)
  |   |-- rag_engine.py           (RAG pipeline)
  |   |-- vector_store.py         (Vector search)
  |   |-- pdf_processor.py        (PDF handling)
  |-- frontend/
  |   |-- index.html              (Complete UI)
  |-- electron/
  |   |-- main.js                 (Desktop app main process)
  |   |-- preload.js              (Desktop app preload script)

---

Offline Capability

Why It Is Fully Offline:
1. Ollama runs locally — no API calls to external services
2. All data stored locally — SQLite database and vector store on disk
3. Frontend is static HTML — no external dependencies at runtime
4. AI model downloaded once and runs indefinitely offline

Internet is only needed for:
- Initial setup (installing packages and downloading the AI model)

---

Performance

- Chat Response: 2-10 seconds (CPU and model dependent)
- PDF Processing: ~5 seconds per page
- Vector Search: Less than 1 second
- Database Queries: Less than 100 milliseconds
