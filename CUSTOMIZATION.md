# 🎨 Customization Guide

Want to make this chatbot your own? Here's how to customize it!

---

## 🎨 Changing Colors

Open `frontend/index.html` and find the `<style>` section. Here are the main colors you can change:

### **Background Gradient**
```css
/* Line ~28 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Try these beautiful gradients:**
```css
/* Ocean Blue */
background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);

/* Sunset Orange */
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

/* Forest Green */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);

/* Dark Mode */
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
```

### **Message Bubble Colors**
```css
/* User messages - Line ~220 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Bot messages - Line ~228 */
background: white;
color: #2d3748;
```

---

## 🤖 Changing the AI Model

Want to use a different AI model?

### **Step 1: Download a New Model**
```bash
ollama pull mistral       # Fast and efficient
ollama pull codellama     # Great for coding
ollama pull gemma:7b      # Google's model
ollama pull llama3.1:70b  # More powerful (needs 40GB RAM)
```

### **Step 2: Update the Backend**
Open `backend/app.py` and change line 24:
```python
DEFAULT_MODEL = "mistral"  # Change from "llama3.2"
```

### **Step 3: Restart the Server**
Stop the backend (Ctrl+C) and run it again:
```bash
python backend/app.py
```

---

## 📝 Adding a Custom System Prompt

Want to give your AI a personality? Add a system prompt!

Open `backend/app.py` and modify the `/chat` route (around line 47):

```python
# Add this configuration
SYSTEM_PROMPT = "You are a helpful coding assistant who explains things simply."

# Then modify the payload (around line 65)
payload = {
    "model": DEFAULT_MODEL,
    "prompt": f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:",
    "stream": False
}
```

**Example Prompts:**
- "You are a friendly teacher who uses lots of emojis"
- "You are a professional blockchain expert"
- "You are a coding mentor who gives examples"
- "You are a creative writer who tells stories"

---

## 🎭 Changing the Chat Title

Open `frontend/index.html` and find line 449:
```html
<h1>AI Chatbot</h1>
<p>Powered by Ollama - Running Locally</p>
```

Change to whatever you want:
```html
<h1>My Smart Assistant</h1>
<p>Your Personal AI Helper</p>
```

Or make it project-specific:
```html
<h1>Blockchain Helper</h1>
<p>Ask me anything about blockchain!</p>
```

---

## 💬 Adding More Quick Prompts

Find the quick prompts section (around line 467) and add your own:

```html
<button class="quick-prompt-btn" onclick="sendQuickMessage('Your question here')">
    🔥 Your Label
</button>
```

**Examples:**
```html
<button class="quick-prompt-btn" onclick="sendQuickMessage('Explain smart contracts')">
    🔗 Smart Contracts
</button>

<button class="quick-prompt-btn" onclick="sendQuickMessage('Help me debug Python code')">
    🐛 Debug Code
</button>
```

---

## 🎵 Adding Sounds

Want a sound notification when the AI responds?

Add this to `frontend/index.html` inside the `<head>` section:
```html
<audio id="notificationSound" src="https://assets.mixkit.co/active_storage/sfx/2354/2354-preview.mp3" preload="auto"></audio>
```

Then in the JavaScript, find the `addMessage` function and add:
```javascript
function addMessage(text, sender) {
    // ... existing code ...
    
    // Play sound for bot messages
    if (sender === 'bot') {
        document.getElementById('notificationSound').play();
    }
}
```

---

## 💾 Adding Chat History (Save Conversations)

To save conversations to a file, add this to `backend/app.py`:

```python
import json
from datetime import datetime

# After the /chat route function, add:
def save_conversation(user_msg, bot_msg):
    try:
        # Load existing conversations
        try:
            with open('conversations.json', 'r') as f:
                conversations = json.load(f)
        except FileNotFoundError:
            conversations = []
        
        # Add new conversation
        conversations.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_msg,
            'bot': bot_msg
        })
        
        # Save back to file
        with open('conversations.json', 'w') as f:
            json.dump(conversations, f, indent=2)
    except Exception as e:
        print(f"Error saving conversation: {e}")

# Then in the /chat route, after getting ai_response, add:
save_conversation(user_message, ai_response)
```

---

## 🌐 Changing the Port

If port 5000 is already in use, change it:

In `backend/app.py`, line ~end:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Changed from 5000
```

In `frontend/index.html`, line ~508:
```javascript
const API_URL = 'http://localhost:5001/chat';  // Changed from 5000
```

---

## 📱 Making it Mobile-Friendly

The chatbot is already responsive! Test it by:
1. Opening in your browser
2. Pressing F12 (Developer Tools)
3. Clicking the mobile icon
4. Selecting a phone size

It automatically adjusts for mobile screens! 📱

---

## 🎨 Advanced: Custom Themes

Want a complete theme change? Here are some ready-to-use themes:

### **Dark Mode Theme**
Replace the gradient in `body` style:
```css
body {
    background: #1a1a2e;
}

.chat-container {
    background: rgba(22, 27, 34, 0.95);
}

.chat-messages {
    background: #0d1117;
}

.bot-message {
    background: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
}
```

### **Minimalist White Theme**
```css
body {
    background: #f5f5f5;
}

.chat-header {
    background: white;
    color: #333;
    border-bottom: 2px solid #e0e0e0;
}

.user-message {
    background: #333;
}
```

---

## 🔧 Need More Help?

Check out:
- `README.md` - Full documentation
- `QUICKSTART.md` - Setup instructions
- `backend/app.py` - All the backend code with comments
- `frontend/index.html` - All the frontend code with comments

**Happy customizing! 🎨**
