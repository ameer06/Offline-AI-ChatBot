Customization Guide

LexaMind — Offline AI Chatbot with RAG

---

Changing Colors

Open frontend/index.html and locate the <style> section. The primary colors used are:

- Background: #212121 (dark gray)
- Accent: #8e44ad (purple)
- Text: #ececec (light gray)
- Input: #2a2a2a (dark input fields)

To change the accent color, search for "#8e44ad" in index.html and replace all instances with your preferred color.

Example color schemes:
- Ocean Blue: #2193b0
- Emerald Green: #11998e
- Sunset Orange: #f5576c
- Royal Blue: #667eea

---

Changing the AI Model

Step 1: Download a new model
  ollama pull mistral       (fast and efficient)
  ollama pull codellama     (optimized for coding)
  ollama pull gemma2:2b     (Google's compact model)

Step 2: Update the default model
  Open backend/app.py and change line 46:
    DEFAULT_MODEL = "mistral"

Step 3: Restart the server
  Stop the backend (Ctrl+C) and run it again:
    python backend/app.py

Alternatively, use the model dropdown in the application header to switch models at runtime without modifying code.

---

Adding a Custom System Prompt

To give the AI a specific personality, open backend/app.py and add a system prompt configuration:

  SYSTEM_PROMPT = "You are a helpful coding assistant who explains things simply."

Then modify the chat prompt to include it:

  prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"

Example system prompts:
- "You are a professional legal document reviewer."
- "You are a coding mentor who provides examples with every explanation."
- "You are a medical knowledge assistant. Always recommend consulting a professional."
- "You are an academic writing helper focused on clarity and structure."

---

Changing the Port

If port 5000 is already in use:

In backend/app.py (last line):
  app.run(host='0.0.0.0', port=5001, debug=True)

In frontend/index.html, search for "5000" and replace with "5001" (update the API URL).

---

Responsive Design

The chatbot interface is already responsive. To test on mobile:
1. Open the application in your browser
2. Press F12 to open Developer Tools
3. Click the device toggle icon (mobile/tablet)
4. Select a device size to preview

The sidebar automatically collapses into a hamburger menu on smaller screens.

---

Custom Themes

Dark Mode (current default):
  The application ships with a dark theme. All color values are defined in the <style> section of index.html.

Light Mode:
  To create a light theme, modify the primary background and text colors:
    body background: #f5f5f5
    text color: #333333
    input background: #ffffff
    sidebar background: #ffffff
    border color: #e0e0e0

---

Additional Resources

- README.md — Full installation and usage documentation
- QUICKSTART.md — Rapid setup guide
- HOW_IT_WORKS.md — Technical architecture details
- backend/app.py — Backend code with inline comments
- frontend/index.html — Frontend code with inline comments
