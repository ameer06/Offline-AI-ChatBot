# How the Project Works

## Overview

The **Local AI Chatbot with RAG** is a fully offline AI-powered chatbot that uses Retrieval Augmented Generation (RAG) to answer questions based on your uploaded PDF documents, while also functioning as a general-purpose chatbot.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND                            │
│  (HTML/CSS/JavaScript - index.html)                     │
│  - User Interface                                       │
│  - Chat Display                                         │
│  - Document Management                                  │
│  - Theme Toggle, Sidebar                                │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP Requests (Port 5000)
                   ▼
┌─────────────────────────────────────────────────────────┐
│                     BACKEND                             │
│  (Python Flask - app.py)                                │
│  - REST API Endpoints                                   │
│  - Request Routing                                      │
│  - Business Logic                                       │
└─────┬─────────┬──────────┬──────────────────────────────┘
      │         │          │
      ▼         ▼          ▼
┌──────────┐ ┌────────┐ ┌─────────────┐
│ Database │ │  RAG   │ │   Ollama    │
│ (SQLite) │ │ Engine │ │  (AI Model) │
└──────────┘ └────────┘ └─────────────┘
      │           │            │
      │           ▼            │
      │    ┌─────────────┐    │
      │    │ Vector Store│    │
      │    │  (ChromaDB) │    │
      │    └─────────────┘    │
      │           │            │
      │           ▼            │
      │    ┌─────────────┐    │
      │    │PDF Processor│    │
      │    └─────────────┘    │
      │                       │
      └───────────────────────┘
```

---

## Component Breakdown

### 1. **Frontend** (`frontend/index.html`)

**Purpose**: User interface for interaction

**Key Features**:
- Chat interface with message display
- PDF upload button
- Sidebar with chat history and documents
- Dark/light mode toggle
- Model selection dropdown

**Technologies**:
- HTML5
- CSS3 (with animations)
- Vanilla JavaScript
- Marked.js (Markdown rendering)
- Highlight.js (Code syntax highlighting)

---

### 2. **Backend API** (`backend/app.py`)

**Purpose**: Handles all server-side logic

**Main Endpoints**:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chat` | POST | Send message, get AI response |
| `/api/documents/upload` | POST | Upload PDF file |
| `/api/documents` | GET | List all documents |
| `/api/documents/<id>` | DELETE | Delete a document |
| `/api/conversations/new` | POST | Create new chat |
| `/api/conversations` | GET | List all chats |
| `/api/models` | GET | List available AI models |

**Technologies**:
- Flask (Web framework)
- Flask-CORS (Cross-origin requests)
- Requests (HTTP calls to Ollama)

---

### 3. **Database** (`backend/database.py`)

**Purpose**: Store chat history and metadata

**Schema**:

```sql
Conversations Table:
- id (PRIMARY KEY)
- title
- model_name
- created_at

Messages Table:
- id (PRIMARY KEY)
- conversation_id (FOREIGN KEY)
- role (user/assistant)
- content
- has_rag_context
- created_at

Documents Table:
- id (PRIMARY KEY)
- filename
- file_path
- file_size
- page_count
- uploaded_at
```

**Storage**: SQLite database (`backend/data/chatbot.db`)

---

### 4. **RAG Engine** (`backend/rag_engine.py`)

**Purpose**: Retrieval Augmented Generation pipeline

**Workflow**:

```
User Query
    ↓
1. Retrieve Context (search vector store)
    ↓
2. Build Enhanced Prompt (add relevant chunks)
    ↓
3. Generate Response (send to Ollama)
    ↓
AI Response
```

**Key Methods**:
- `retrieve_context()` - Find relevant PDF chunks
- `build_prompt_with_context()` - Create enhanced prompt
- `generate_response()` - Get AI response
- `chat_with_rag()` - Complete pipeline

---

### 5. **Vector Store** (`backend/vector_store.py`)

**Purpose**: Store and search document embeddings

**How It Works**:
1. PDF text is split into chunks (512 chars)
2. Each chunk is converted to embeddings (vectors)
3. Stored in ChromaDB for fast semantic search
4. Query → Find similar chunks → Return to RAG

**Storage**: `backend/data/chroma_db/`

**Technology**: ChromaDB + Sentence Transformers

---

### 6. **PDF Processor** (`backend/pdf_processor.py`)

**Purpose**: Extract and chunk PDF text

**Process**:
1. Upload PDF → Save to `backend/data/uploads/`
2. Extract text using PyPDF2
3. Split into chunks (512 chars, 50 overlap)
4. Return chunks with metadata

**Input**: PDF file  
**Output**: List of text chunks + metadata

---

### 7. **Ollama Integration**

**Purpose**: Run AI models locally

**How It Works**:
- Ollama runs as a separate service (port 11434)
- Backend sends HTTP POST requests to Ollama
- Ollama processes prompts and returns responses
- Fully offline - no internet needed

**API Call**:
```json
POST http://localhost:11434/api/generate
{
  "model": "llama3.2",
  "prompt": "Your question here",
  "stream": false
}
```

---

## Data Flow

### Scenario 1: Normal Chat (No RAG)

```
User types message
    ↓
Frontend sends to /chat
    ↓
Backend forwards to Ollama
    ↓
Ollama generates response
    ↓
Backend saves to database
    ↓
Response sent to frontend
    ↓
Displayed in chat
```

### Scenario 2: RAG-Enhanced Chat

```
User types question (with docs uploaded)
    ↓
Frontend sends to /chat with use_rag=true
    ↓
Backend → RAG Engine
    ↓
RAG searches vector store for relevant chunks
    ↓
RAG builds enhanced prompt with context
    ↓
Enhanced prompt sent to Ollama
    ↓
Ollama generates context-aware response
    ↓
Response + metadata saved to database
    ↓
Response sent to frontend with RAG badge
    ↓
Displayed in chat (with "RAG" indicator)
```

### Scenario 3: PDF Upload

```
User selects PDF file
    ↓
Frontend sends file to /api/documents/upload
    ↓
Backend saves PDF to uploads/
    ↓
PDF Processor extracts text
    ↓
Text chunked into pieces
    ↓
Chunks converted to embeddings
    ↓
Embeddings stored in ChromaDB
    ↓
Document metadata saved to database
    ↓
Success response to frontend
    ↓
Document appears in sidebar
```

---

## Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | HTML/CSS/JS | User interface |
| Backend | Flask (Python) | API server |
| Database | SQLite | Chat history |
| Vector DB | ChromaDB | Document embeddings |
| AI Model | Ollama (llama3.2) | Text generation |
| PDF Parser | PyPDF2 | Extract text |
| Embeddings | Sentence Transformers | Text to vectors |
| Markdown | Marked.js | Render formatted text |
| Syntax | Highlight.js | Code highlighting |

---

## Storage Locations

```
Local AI-Chatbot/
├── backend/
│   ├── data/
│   │   ├── chatbot.db          ← SQLite database
│   │   ├── uploads/            ← Uploaded PDFs
│   │   └── chroma_db/          ← Vector embeddings
│   ├── app.py                  ← Main backend
│   ├── database.py             ← Database ops
│   ├── rag_engine.py           ← RAG pipeline
│   ├── vector_store.py         ← Vector DB ops
│   └── pdf_processor.py        ← PDF handling
└── frontend/
    └── index.html              ← Complete UI
```

---

## Offline Capability

**Why It's Fully Offline**:
1. ✅ Ollama runs locally (no API calls to cloud)
2. ✅ All data stored locally (SQLite, ChromaDB)
3. ✅ Frontend is static HTML (no external dependencies)
4. ✅ AI model downloaded once, runs forever offline

**Internet only needed for**:
- Initial setup (install packages, download model)
- That's it!

---

## Performance

- **Chat Response**: 2-10 seconds (CPU-dependent)
- **PDF Upload**: ~5 seconds per page
- **Vector Search**: <1 second
- **Database Queries**: <100ms

---

## Summary

Your chatbot is a **full-stack application** that combines:
- Modern web UI (Frontend)
- RESTful API (Backend)
- Local AI inference (Ollama)
- Semantic search (RAG + ChromaDB)
- Persistent storage (SQLite)

All working together to create an **intelligent, offline-capable chatbot** that learns from your documents!
