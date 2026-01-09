# System Requirements

## Hardware Requirements

### Minimum Requirements
- **CPU**: Intel Core i5 / AMD Ryzen 5 (4 cores)
- **RAM**: 8 GB
- **Storage**: 10 GB free space
- **GPU**: Not required (CPU-only)

### Recommended Requirements
- **CPU**: Intel Core i7 / AMD Ryzen 7 (8 cores)
- **RAM**: 16 GB or higher
- **Storage**: 20 GB SSD free space
- **GPU**: NVIDIA GPU with 6GB+ VRAM (for faster inference - optional)

---

## Software Requirements

### Operating System
- Windows 10/11 (64-bit)
- macOS 10.15+
- Linux (Ubuntu 20.04+ or equivalent)

### Required Software

#### 1. **Python**
- Version: **3.8 or higher** (3.10+ recommended)
- Download: https://www.python.org/downloads/

#### 2. **Ollama**
- Latest version
- Download: https://ollama.ai/download
- Purpose: Runs local AI models offline

#### 3. **Web Browser**
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

---

## Python Dependencies

Install via `pip install -r requirements.txt`:

```
Flask==2.3.0
Flask-CORS==4.0.0
PyPDF2==3.0.1
chromadb==0.4.15
sentence-transformers==2.2.2
requests==2.31.0
```

---

## AI Models Required

### Default Model
- **Model**: `llama3.2` (or any Ollama model)
- **Size**: ~2-4 GB
- **Installation**: 
  ```bash
  ollama pull llama3.2
  ```

### Alternative Models (Optional)
- `llama2` - 7GB
- `mistral` - 4GB
- `phi` - 2GB

---

## Network Requirements

- **Internet**: Required only for initial setup (downloading dependencies and models)
- **After Setup**: Fully offline - no internet needed
- **Ports**: 
  - Backend: `5000` (Flask API)
  - Ollama: `11434` (Default Ollama port)

---

## Quick Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Ollama installed and running
- [ ] AI model downloaded (`ollama pull llama3.2`)
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Port 5000 and 11434 available

---

## Storage Space Breakdown

| Component | Size |
|-----------|------|
| Python Dependencies | ~500 MB |
| AI Model (llama3.2) | ~2 GB |
| ChromaDB Vector Store | Varies (depends on PDFs) |
| Uploaded PDFs | User dependent |
| **Total (Minimum)** | **~3 GB** |

---

## Performance Notes

- **Chat Response Time**: 2-10 seconds (depends on CPU/model)
- **PDF Processing**: ~5 seconds per page
- **Concurrent Users**: 1 (local deployment)
- **Document Limit**: No hard limit (memory dependent)

---

## Compatibility

✅ **Works On**:
- Windows 10/11
- macOS (Intel & Apple Silicon)
- Linux (Ubuntu, Fedora, etc.)

❌ **Not Supported**:
- Mobile devices (Android/iOS)
- Windows 7 or older
- 32-bit systems
