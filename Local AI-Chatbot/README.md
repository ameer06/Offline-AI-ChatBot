LexaMind — Offline AI Chatbot with RAG

A locally-running AI chatbot powered by Ollama — completely free, fully offline, with Retrieval Augmented Generation (RAG) and Study Assistant capabilities.

---

Prerequisites

Before starting, install the following on your computer:

1. Python (Programming Language)
   - Download: https://www.python.org/downloads/
   - Version: Python 3.8 or higher
   - Important: During installation, check the box "Add Python to PATH"

2. Ollama (Local AI Engine)
   - Download: https://ollama.com/download
   - Select the Windows version and install
   - After installation, it runs in the background

3. Git (Optional)
   - Download: https://git-scm.com/downloads
   - Alternatively, download the project as a ZIP file

---

Installation

Step 1: Download the Project

Using Git:
  Open PowerShell or Command Prompt:
    cd Desktop
    git clone <repository-url>
    cd LexaMind

Without Git:
  1. Download the project as a ZIP file
  2. Extract it to your Desktop
  3. Open the folder

Step 2: Install Python Packages

Open PowerShell in the project folder:

  python -m pip install flask flask-cors requests PyPDF2 numpy

Note: If you receive a "pip not recognized" error, use "python -m pip" instead of "pip".

Step 3: Download an AI Model

  ollama pull llama3.2

This downloads the Llama 3.2 model (~2 GB). Estimated time: 5-15 minutes depending on internet speed.

Other model options (install later as needed):
  ollama pull llama3.2:1b    (smallest, fastest — 1.3 GB)
  ollama pull mistral        (fast, balanced — 4 GB)
  ollama pull codellama      (coding specialist — 4 GB)
  ollama pull gemma2:2b      (Google's compact model — 1.6 GB)

Step 4: Verify Ollama

  ollama run llama3.2

Type a message to test. Type /bye to exit.

---

Running the Chatbot

1. Start the Backend Server

Open PowerShell in the project folder:

  python backend/app.py

You should see:
  Running on http://127.0.0.1:5000

Keep this window open. The server must remain running.

2. Open the Chat Interface

Option A: Double-click frontend/index.html to open in your browser
Option B: Open your browser and navigate to File > Open > frontend/index.html

3. Start Chatting

Type a message and press Enter or click Send.

---

Features

- AI-powered chat with markdown and code rendering
- Multi-conversation management with persistent history
- PDF upload and processing for document-based Q&A (RAG)
- Selective document querying — choose which PDFs to search
- Study Assistant — AI-generated summaries, quizzes, and flashcards
- Model switching between installed Ollama models
- Dark mode interface with responsive design
- Desktop application packaging via Electron
- Complete offline operation after initial setup
- Privacy-focused — all data stays on your machine

---

Project Structure

  LexaMind/
  |
  |-- backend/
  |   |-- app.py              (Flask API server — 27 endpoints)
  |   |-- database.py         (SQLite database manager)
  |   |-- rag_engine.py       (RAG pipeline orchestrator)
  |   |-- vector_store.py     (Cosine similarity vector search)
  |   |-- pdf_processor.py    (PDF text extraction and chunking)
  |   |-- requirements.txt    (Python dependencies)
  |
  |-- frontend/
  |   |-- index.html          (Complete UI — HTML, CSS, JavaScript)
  |
  |-- electron/
  |   |-- main.js             (Electron main process)
  |   |-- preload.js          (Electron preload script)
  |
  |-- data/
  |   |-- chatbot.db          (SQLite database)
  |   |-- uploads/            (Uploaded PDF storage)
  |
  |-- README.md
  |-- ABSTRACT.md
  |-- HOW_IT_WORKS.md
  |-- SYSTEM_REQUIREMENTS.md
  |-- QUICKSTART.md
  |-- CUSTOMIZATION.md
  |-- PROJECT_FAQ.md
  |-- PROJECT_SUBMISSION.md
  |-- README_DESKTOP.md
  |-- package.json            (Node.js dependencies for Electron)
  |-- install.bat             (Windows installer script)
  |-- launch_chatbot.bat      (Launch script)
  |-- start_all.bat           (Start backend + frontend)

---

How It Works

1. Frontend (index.html): The user interface displayed in the browser
2. Backend (app.py): A Python Flask server that receives messages and routes requests
3. Ollama: The AI inference engine running the language model locally
4. Flow: User types message > Frontend sends to Backend > Backend queries Ollama > Ollama generates response > Response returned to user

  +---------------+      +---------------+      +---------------+
  |    Browser    | ---> |    Backend    | ---> |    Ollama     |
  |  (Frontend)   | <--- |   (Python)    | <--- |  (AI Model)   |
  +---------------+      +---------------+      +---------------+

---

Troubleshooting

"Python is not recognized"
  Uninstall Python, reinstall, and check "Add Python to PATH" during installation.

"ollama: command not found"
  Download Ollama from https://ollama.com/download. Restart your computer after installation.

"Connection refused" in backend
  Verify Ollama is running: ollama list
  If models are listed, Ollama is operational. Otherwise, restart Ollama.

"Error: Could not connect to chatbot"
  Ensure the backend server is running with: python backend/app.py
  Confirm you see "Running on http://127.0.0.1:5000".

Slow model responses
  First response is slower (model is loading into memory).
  Try a smaller model: ollama pull llama3.2:1b
  Close other applications to free RAM. Minimum 8 GB recommended.

---

Model Options

  llama3.2      — Best all-around choice (recommended)
  llama3.2:1b   — Smallest and fastest
  mistral       — Good balance of speed and quality
  codellama     — Best for programming questions

Performance Tips:
  - First response takes longer as the model loads into memory
  - Close unnecessary applications to free up RAM
  - Smaller models produce faster responses

---

Command Reference

  python --version                          (Check Python version)
  python -m pip install flask flask-cors    (Install Python packages)
  ollama list                               (List downloaded models)
  ollama pull llama3.2                      (Download a model)
  ollama run llama3.2                       (Test a model)
  python backend/app.py                     (Start the backend server)
  ollama rm llama3.2                        (Remove a model)

---

License

This project is free to use, modify, and distribute.
