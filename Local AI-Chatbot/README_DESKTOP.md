Desktop Application — Installation and Usage

LexaMind — Offline AI Chatbot with RAG

---

Overview

LexaMind is available as a standalone desktop application built with Electron. The desktop version provides a native application experience — no need to manually open HTML files or run commands. Simply launch the application and start using it.

Features:
- Desktop application with custom window controls
- Automatic backend server startup
- Model selector dropdown for switching between AI models
- Professional native application interface
- All features of the web version included

---

Installation

1. Install Node.js

Download and install Node.js from: https://nodejs.org/
Select the LTS (Long Term Support) version.

2. Install Dependencies

Open PowerShell in the project folder and run:

  npm install

This installs Electron and other required Node.js packages.

---

Running the Desktop App

Development Mode:

  npm start

This will:
1. Launch the desktop application window
2. Automatically start the Python backend server
3. Load the chat interface

Building an Installer (for distribution):

  npm run build:win

This creates a Windows installer (.exe) in the dist/ folder.

---

Usage

1. Model Selection: Use the dropdown in the application header to switch between installed AI models (llama3.2, mistral, codellama, etc.)

2. Downloading Models: Before using a model, download it via PowerShell:
     ollama pull llama3.2
     ollama pull mistral

3. Switching Models: Select a different model from the dropdown — the application switches automatically.

---

Project Structure

  LexaMind/
  |-- electron/
  |   |-- main.js             (Electron main process)
  |   |-- preload.js          (Secure IPC bridge)
  |-- frontend/
  |   |-- index.html          (Chat interface)
  |-- backend/
  |   |-- app.py              (Flask API server)
  |   |-- database.py         (Database manager)
  |   |-- rag_engine.py       (RAG pipeline)
  |   |-- vector_store.py     (Vector search)
  |   |-- pdf_processor.py    (PDF processing)
  |-- package.json            (Node.js dependencies)

---

Troubleshooting

"npm is not recognized"
  Node.js is not installed or not in PATH.
  Install from https://nodejs.org/ and restart your terminal.

"Cannot find module 'electron'"
  Run: npm install

Backend not starting
  Verify Python is installed.
  Verify Flask is installed: python -m pip install flask flask-cors requests

Model not showing in dropdown
  Ensure Ollama is running.
  Download at least one model: ollama pull llama3.2

---

Distribution

To share the application with others:

1. Build the installer: npm run build:win
2. Locate the installer in the dist/ folder
3. Share the .exe file

User requirements:
- Windows operating system
- Python 3.8+ installed
- Ollama installed and running
- At least one AI model downloaded

---

Command Reference

  npm start                   (Run in development mode)
  npm run build               (Build for current platform)
  npm run build:win           (Build Windows installer)
  npm install                 (Install/update dependencies)
