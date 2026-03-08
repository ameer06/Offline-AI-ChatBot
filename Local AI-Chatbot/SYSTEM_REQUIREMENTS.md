System Requirements

LexaMind — Offline AI Chatbot with RAG

---

Hardware Requirements

Minimum Requirements
- CPU: Intel Core i5 / AMD Ryzen 5 (4 cores)
- RAM: 8 GB
- Storage: 10 GB free space
- GPU: Not required (CPU-only mode supported)

Recommended Requirements
- CPU: Intel Core i7 / AMD Ryzen 7 (8 cores)
- RAM: 16 GB or higher
- Storage: 20 GB SSD free space
- GPU: NVIDIA GPU with 6GB+ VRAM (optional, for faster inference)

---

Software Requirements

Operating System
- Windows 10/11 (64-bit)
- macOS 10.15+
- Linux (Ubuntu 20.04+ or equivalent)

Required Software

1. Python
   - Version: 3.8 or higher (3.10+ recommended)
   - Download: https://www.python.org/downloads/

2. Ollama
   - Latest version
   - Download: https://ollama.ai/download
   - Purpose: Runs local AI models offline

3. Node.js (for Desktop App only)
   - LTS version recommended
   - Download: https://nodejs.org/

4. Web Browser
   - Chrome 90+, Firefox 88+, Edge 90+, or Safari 14+

---

Python Dependencies

Install via: pip install -r requirements.txt

  Flask==2.3.0
  Flask-CORS==4.0.0
  PyPDF2==3.0.1
  requests==2.31.0
  numpy

---

AI Models

Default Model
- Model: llama3.2
- Size: ~2-4 GB
- Installation: ollama pull llama3.2

Alternative Models (Optional)
- mistral — 4 GB, good balance of speed and quality
- codellama — 4 GB, optimized for coding tasks
- llama3.2:1b — 1.3 GB, fastest and most lightweight
- gemma2:2b — 1.6 GB, Google's compact model

---

Network Requirements

- Internet: Required only for initial setup (downloading dependencies and models)
- After Setup: Fully offline — no internet connection needed
- Ports Used:
  - Port 5000: Flask backend API
  - Port 11434: Ollama inference engine

---

Storage Space Breakdown

| Component               | Size                        |
|-------------------------|-----------------------------|
| Python Dependencies     | ~500 MB                     |
| AI Model (llama3.2)     | ~2 GB                       |
| Vector Store            | Varies (depends on PDFs)    |
| Uploaded PDFs           | User dependent              |
| Total (Minimum)         | ~3 GB                       |

---

Performance Notes

- Chat Response Time: 2-10 seconds (depends on CPU and model)
- PDF Processing: ~5 seconds per page
- Vector Search: Less than 1 second
- Concurrent Users: 1 (local deployment)
- Document Limit: No hard limit (memory dependent)

---

Compatibility

Supported:
- Windows 10/11
- macOS (Intel and Apple Silicon)
- Linux (Ubuntu, Fedora, etc.)

Not Supported:
- Mobile devices (Android/iOS)
- Windows 7 or older
- 32-bit systems

---

Setup Checklist

- Python 3.8+ installed
- Ollama installed and running
- AI model downloaded (ollama pull llama3.2)
- Python dependencies installed (pip install -r requirements.txt)
- Ports 5000 and 11434 available
