# 🖥️ Desktop App - Installation & Usage

## What's New?

Your AI Chatbot is now a **standalone desktop application**! No need to manually open HTML files or run Python commands - just double-click and go!

## New Features

✅ **Desktop Application** - Runs like any other app (Chrome, Spotify, etc.)
✅ **Model Selector** - Choose which AI model to use from a dropdown
✅ **Auto-Start Backend** - Backend server starts automatically
✅ **Professional Interface** - Clean, modern desktop app experience
✅ **System Tray Integration** - Minimize to system tray (optional)

---

## Installation

### 1. Install Node.js (Required for Electron)

Download and install Node.js from: https://nodejs.org/

**Recommended**: LTS version (Long Term Support)

### 2. Install Desktop App Dependencies

Open PowerShell in the project folder and run:

```bash
npm install
```

This will install Electron and other dependencies needed for the desktop app.

---

## Running the Desktop App

### Development Mode (For Testing)

```bash
npm start
```

This will:
1. Launch the desktop app window
2. Automatically start the Python backend
3. Load the chat interface

### Build Installer (For Distribution)

```bash
npm run build:win
```

This creates a Windows installer (`.exe`) in the `dist/` folder that you can share with others!

---

## How to Use

### 1. Choose Your Model

In the app header, you'll see a dropdown menu. Click it to select which AI model to use:
- **llama3.2** - Best all-around (default)
- **llama3.2:1b** - Fastest, lightweight
- **mistral** - Good balance
- **codellama** - Best for coding

### 2. Download New Models

To use a model, you need to download it first.

**From Terminal/PowerShell:**
```bash
ollama pull llama3.2
ollama pull mistral
ollama pull codellama
```

**From Python (Future Feature):**
We can add an in-app download button in the next update!

### 3. Switch Models

Just select a different model from the dropdown - the app will automatically switch!

---

## Project Structure

```
ai-chatbot/
│
├── electron/              # Desktop app files
│   ├── main.js           # Electron main process
│   └── preload.js        # Secure IPC bridge
│
├── frontend/             # UI (HTML/CSS/JS)
│   └── index.html        # Chat interface
│
├── backend/              # Python Flask server
│   └── app.py            # API with model management
│
├── package.json          # Node.js dependencies
└── README_DESKTOP.md     # This file!
```

---

## Troubleshooting

### "npm is not recognized"
- Node.js is not installed or not in PATH
- Install Node.js from nodejs.org
- Restart your terminal

### "Cannot find module 'electron'"
```bash
npm install
```

### Backend not starting
- Make sure Python is installed
- Make sure Flask is installed: `python -m pip install flask flask-cors requests`

### Model not showing in dropdown
- Make sure Ollama is running
- Download at least one model: `ollama pull llama3.2`

---

## Distribution

To share your app with others:

1. Build the installer:
   ```bash
   npm run build:win
   ```

2. Find the installer in `dist/` folder

3. Share the `.exe` file!

**Requirements for users:**
- Windows OS
- Python installed
- Ollama installed
- At least one AI model downloaded

---

## Future Enhancements (Ideas)

- [ ] In-app model download with progress bar
- [ ] Dark mode toggle
- [ ] Chat history/save conversations
- [ ] Export chat to PDF
- [ ] Voice input/output
- [ ] Multiple chat sessions
- [ ] Custom AI personalities

---

## Commands Quick Reference

```bash
# Development
npm start                 # Run in dev mode

# Building
npm run build            # Build for current platform
npm run build:win        # Build Windows installer

# Dependencies
npm install              # Install/update dependencies
```

---

## Need Help?

Check the main README.md for more details about the chatbot itself!
