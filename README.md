# 🤖 AI Chatbot - Complete Beginner's Guide

A beautiful, locally-running AI chatbot powered by **Ollama** - completely FREE and works offline!

![Chatbot Preview](https://img.shields.io/badge/Status-Ready-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-Free-green?style=for-the-badge)

---

## 📋 What You'll Need to Install

Before we start, you need to install 3 things on your computer:

### 1️⃣ **Python** (The programming language)
- **Download from:** https://www.python.org/downloads/
- **Version needed:** Python 3.8 or higher
- ⚠️ **IMPORTANT:** When installing, CHECK the box that says "Add Python to PATH"

### 2️⃣ **Ollama** (Runs AI models locally)
- **Download from:** https://ollama.com/download
- Choose "Windows" version and install it
- After installation, it will run in the background

### 3️⃣ **Git** (Optional - for downloading code easily)
- **Download from:** https://git-scm.com/downloads
- Or you can just download the project as a ZIP file

---

## 🚀 Step-by-Step Installation

### **Step 1: Download This Project**

**Option A: Using Git** (if you installed it)
```bash
# Open PowerShell or Command Prompt
# Navigate to your Desktop or preferred location
cd Desktop

# Clone this project
git clone <your-repository-url>
cd ai-chatbot
```

**Option B: Without Git**
1. Download the project as a ZIP file
2. Extract it to your Desktop
3. Open the folder

---

### **Step 2: Install Python Packages**

Open **PowerShell** or **Command Prompt** in the project folder:

```bash
# Install required Python libraries
python -m pip install flask flask-cors requests
```

> 💡 **What this does:** Installs the necessary tools for the chatbot to work
> 
> ⚠️ **Note:** If you get a "pip is not recognized" error, use `python -m pip` instead of just `pip`

---

### **Step 3: Download an AI Model**

Open **PowerShell** and run:

```bash
# Download Llama 3.2 model (about 2GB)
ollama pull llama3.2
```

> ⏱️ **This will take 5-15 minutes** depending on your internet speed
> 
> 💡 **What this does:** Downloads the AI brain that powers your chatbot

**Other model options** (you can try these later):
```bash
ollama pull llama3.2:1b    # Smallest, fastest model (1.3GB)
ollama pull mistral        # Faster, smaller model (4GB)
ollama pull llama3.1       # More powerful version (4.7GB)
ollama pull gemma2:2b      # Google's small model (1.6GB)
```

---

### **Step 4: Test if Ollama is Working**

```bash
ollama run llama3.2
```

You should see a prompt where you can chat with the AI. Type something like "Hello!"

To exit, type `/bye`

---

## ▶️ How to Run the Chatbot

### **1. Start the Backend Server**

Open **PowerShell** in the project folder and run:

```bash
python backend/app.py
```

✅ **You should see:**
```
 * Running on http://127.0.0.1:5000
 * Running on all addresses
 * Running on http://192.168.x.x:5000
```

> ⚠️ **Keep this window open!** The server needs to keep running.

---

### **2. Open the Chatbot Interface**

**Option A: Double-click the file**
- Go to the `frontend` folder
- Double-click `index.html`
- It will open in your default browser

**Option B: Use the path**
- Open your browser (Chrome, Edge, Firefox)
- Press `Ctrl + O` or go to File → Open
- Navigate to the project folder → `frontend` → `index.html`

---

### **3. Start Chatting! 🎉**

You should now see a beautiful chat interface. Type a message and press Enter or click Send!

---

## 🎨 What You Get

✅ Beautiful, modern chat interface  
✅ Real-time AI responses  
✅ Completely FREE - no API keys needed  
✅ Works offline - no internet required after setup  
✅ Privacy-focused - all data stays on your computer  
✅ Customizable - change colors, models, and features  

---

## 🛠️ Troubleshooting

### **Problem: "Python is not recognized"**
**Solution:** You didn't add Python to PATH during installation
- Uninstall Python
- Reinstall it and CHECK the "Add Python to PATH" box

---

### **Problem: "ollama: command not found"**
**Solution:** Ollama is not installed or not running
- Download from https://ollama.com/download
- After installation, restart your computer
- Check if Ollama is running (look for its icon in the system tray)

---

### **Problem: Backend shows "Connection refused"**
**Solution:** Ollama service is not running
```bash
# Check if Ollama is running
ollama list

# If it shows models, Ollama is working
# If not, restart Ollama application
```

---

### **Problem: Chat shows "Error: Could not connect to chatbot"**
**Solution:** Backend server is not running
- Make sure you ran `python backend/app.py`
- Check that you see "Running on http://127.0.0.1:5000"
- Don't close that terminal window

---

### **Problem: Model takes too long to respond**
**Solution:** 
- First response is always slower (model is loading)
- Try a smaller model: `ollama pull mistral`
- Close other heavy applications
- Make sure you have enough RAM (8GB minimum recommended)

---

## 📁 Project Structure

```
ai-chatbot/
│
├── backend/
│   ├── app.py              # Flask server (the brain)
│   └── requirements.txt    # List of needed packages
│
├── frontend/
│   └── index.html          # Chat interface (what you see)
│
└── README.md               # This file!
```

---

## 🎓 How It Works (Simple Explanation)

1. **Frontend (index.html):** The beautiful interface you see in your browser
2. **Backend (app.py):** A Python server that receives your messages
3. **Ollama:** The AI engine running the language model
4. **Flow:** You type → Frontend sends to Backend → Backend asks Ollama → Ollama thinks → Response comes back → You see it!

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Browser   │ ───> │   Backend   │ ───> │   Ollama    │
│  (Frontend) │ <─── │  (Python)   │ <─── │  (AI Model) │
└─────────────┘      └─────────────┘      └─────────────┘
```

---

## 🚀 Next Steps & Improvements

Once you have it working, you can:

- [ ] Change the colors and design in `index.html`
- [ ] Add conversation history (save chats to a database)
- [ ] Try different AI models (`ollama pull codellama` for coding help)
- [ ] Add voice input/output
- [ ] Make it answer questions about your PDF files (RAG)
- [ ] Deploy it online so friends can use it
- [ ] Add user authentication

---

## 💡 Pro Tips

1. **Model Selection:**
   - `llama3.2` - Best all-around choice (recommended)
   - `llama3.2:1b` - Smallest and fastest
   - `mistral` - Good balance of speed and quality
   - `llama3.1` - More powerful, larger model
   - `codellama` - Best for programming questions

2. **Performance:**
   - First response takes longer (model is loading into memory)
   - Close unnecessary apps to free up RAM
   - Smaller models = faster responses

3. **Customization:**
   - Edit colors in the `<style>` section of `index.html`
   - Change the model in `backend/app.py` (line with `"model": "llama3.2"`)
   - Add your own system prompt to give the AI a personality

---

## 🆘 Need Help?

If you get stuck:

1. **Read the error message carefully** - it usually tells you what's wrong
2. **Check the Troubleshooting section** above
3. **Make sure all 3 steps are green:**
   - ✅ Python installed and in PATH
   - ✅ Ollama installed and running
   - ✅ Model downloaded (`ollama list` shows your model)
4. **Verify backend is running** - You should see "Running on http://127.0.0.1:5000"

---

## 📝 Quick Command Reference

```bash
# Check Python version
python --version

# Install Python packages
python -m pip install flask flask-cors requests

# List downloaded models
ollama list

# Download a model
ollama pull llama3.2

# Test a model
ollama run llama3.2

# Start the backend server
python backend/app.py

# Remove a model (to free space)
ollama rm llama3.2
```

---

## 📜 License

This project is completely **FREE** to use, modify, and share! No restrictions.

---

## 🎉 Congratulations!

You've just built your own AI chatbot! This is a great foundation for your final year project. You can expand it with features like:

- Blockchain-based authentication
- Database integration
- Multi-user support
- Custom training on specific topics
- Integration with other services

**Happy Coding! 🚀**
