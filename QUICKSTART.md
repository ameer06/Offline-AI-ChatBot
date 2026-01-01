# 🚀 Quick Start Guide

This is a **super simple** guide to get your chatbot running in 5 minutes!

---

## ✅ Before You Start - Checklist

Make sure you have these installed:

- [ ] **Python 3.8+** - Check by typing `python --version` in PowerShell
- [ ] **Ollama** - Check by typing `ollama --version` in PowerShell
- [ ] **AI Model** - Check by typing `ollama list` in PowerShell

If you don't have these, follow the [Full Installation Guide](README.md#-what-youll-need-to-install).

---

## 🏃 Running the Chatbot (3 Steps)

### Step 1: Install Python Dependencies

Open **PowerShell** in the project folder and run:

```powershell
cd backend
pip install -r requirements.txt
```

⏱️ This takes about 30 seconds.

---

### Step 2: Start the Backend Server

Still in PowerShell, run:

```powershell
python app.py
```

✅ **Success looks like this:**
```
✅ Server is starting...
📍 Server will run at: http://localhost:5000
```

⚠️ **Keep this window open!** Don't close it.

---

### Step 3: Open the Chat Interface

1. Open your **File Explorer**
2. Navigate to the project folder → `frontend` folder
3. **Double-click** `index.html`
4. Your browser will open with the chatbot! 🎉

---

## 💬 Start Chatting!

Type a message and press Enter or click Send. Your first message might take 10-20 seconds as the AI model loads into memory. After that, responses will be faster!

---

## 🛑 To Stop the Chatbot

1. Go back to the PowerShell window
2. Press `Ctrl + C`
3. Close your browser tab

---

## ❌ Common Problems

### "Python is not recognized"
➡️ You need to install Python and add it to PATH. See [README.md](README.md#-step-by-step-installation).

### "Cannot connect to Ollama"
➡️ Type `ollama list` in PowerShell. If you see models listed, Ollama is working. If not, restart your computer after installing Ollama.

### "No module named 'flask'"
➡️ You skipped Step 1. Run `pip install -r requirements.txt` in the backend folder.

### Chat shows "Could not connect to backend"
➡️ The backend server isn't running. Make sure you did Step 2 and see "Running on http://localhost:5000".

---

## 🎨 Try Different Models

Want to try a different AI model?

```powershell
# Download a faster model
ollama pull mistral

# Download a coding specialist
ollama pull codellama
```

Then edit `backend/app.py` and change line 24:
```python
DEFAULT_MODEL = "mistral"  # Change from "llama3.2" to your model
```

Restart the backend server and try it out!

---

## 🎉 You're Done!

Now you have a fully functional AI chatbot running on your computer!

**Next Steps:**
- Customize the colors in `frontend/index.html`
- Add new features like conversation history
- Combine it with your blockchain voting project
- Show it off in your final year presentation! 🚀
