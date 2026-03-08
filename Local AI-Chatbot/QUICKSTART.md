Quick Start Guide

LexaMind — Offline AI Chatbot with RAG

---

Prerequisites

Ensure the following are installed before proceeding:

- Python 3.8+ — Verify with: python --version
- Ollama — Verify with: ollama --version
- AI Model — Verify with: ollama list

If any of these are not installed, refer to the full Installation Guide in README.md.

---

Step 1: Install Python Dependencies

Open PowerShell in the project folder and run:

  cd backend
  pip install -r requirements.txt

This takes approximately 30 seconds.

---

Step 2: Start the Backend Server

In the same terminal, run:

  python app.py

When the server starts successfully, you will see:

  Server is starting...
  Server will run at: http://localhost:5000

Important: Keep this terminal window open. The server must remain running.

---

Step 3: Open the Chat Interface

1. Open File Explorer
2. Navigate to the project folder, then the "frontend" folder
3. Double-click index.html
4. The chatbot will open in your default browser

Alternatively, run the desktop app with: npm start (requires Node.js)

---

Using the Chatbot

Type a message in the input field and press Enter or click Send. The first message may take 10-20 seconds as the AI model loads into memory. Subsequent responses will be faster.

---

Stopping the Chatbot

1. Return to the PowerShell window
2. Press Ctrl + C to stop the server
3. Close the browser tab

---

Troubleshooting

"Python is not recognized"
  Install Python and ensure "Add to PATH" is checked during installation.
  See README.md for detailed instructions.

"Cannot connect to Ollama"
  Run: ollama list
  If models are listed, Ollama is working. If not, restart your computer after installing Ollama.

"No module named 'flask'"
  Run: pip install -r requirements.txt in the backend folder.

"Could not connect to backend"
  Ensure the backend server is running (Step 2) and shows "Running on http://localhost:5000".

---

Trying Different Models

To download and use a different AI model:

  ollama pull mistral       (fast, balanced performance)
  ollama pull codellama     (optimized for coding queries)

After downloading, select the new model from the dropdown menu in the application header. No configuration changes are needed.
