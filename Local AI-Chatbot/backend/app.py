"""
AI Chatbot Backend Server
==========================
This is a simple Flask server that connects your chat interface to Ollama AI.

How it works:
1. Receives messages from the frontend (web interface)
2. Sends them to Ollama (the AI running on your computer)
3. Gets the AI's response
4. Sends it back to the frontend to display

No complicated stuff - just a simple messenger between your browser and the AI!
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from database import Database

# Try to import RAG components (optional)
RAG_AVAILABLE = False
try:
    from pdf_processor import PDFProcessor
    from vector_store import VectorStore
    from rag_engine import RAGEngine
    RAG_AVAILABLE = True
    print("✅ RAG components loaded")
except ImportError as e:
    print(f"⚠️ RAG components not available: {e}")
    print("   Chat history will work, but PDF upload is disabled.")
    print("   To enable RAG: pip install chromadb PyPDF2")

# Create the Flask app (this is your server)
app = Flask(__name__)

# Enable CORS - this allows your HTML page to talk to this server
# Without this, browsers block the connection for security reasons
CORS(app)

# Configuration - you can change these!
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Where Ollama is running
DEFAULT_MODEL = "llama3.2"  # Which AI model to use
UPLOAD_FOLDER = "data/uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {'pdf'}

# Create upload directory
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# Initialize database
db = Database("data/chatbot.db")
print("✅ Database initialized")

# Initialize RAG components (only if available)
if RAG_AVAILABLE:
    try:
        pdf_processor = PDFProcessor(chunk_size=512, chunk_overlap=50)
        vector_store = VectorStore("data/chroma_db")
        rag_engine = RAGEngine(vector_store, OLLAMA_API_URL)
        print("✅ RAG system initialized")
    except Exception as e:
        print(f"⚠️ RAG initialization failed: {e}")
        RAG_AVAILABLE = False

# Global variables
CURRENT_CONVERSATION_ID = None
RAG_ENABLED = RAG_AVAILABLE  # Enable/disable RAG

# You can change the model here to try different ones:
# - "llama3.2" - Best all-around
# - "mistral" - Faster, good for slower computers  
# - "codellama" - Best for coding questions
# - "gemma:7b" - Google's model


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/chat', methods=['POST'])
def chat():
    """
    RAG-ENHANCED chat endpoint (or standard chat if RAG unavailable)
    """
    global CURRENT_CONVERSATION_ID, RAG_ENABLED
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        conversation_id = data.get('conversation_id', CURRENT_CONVERSATION_ID)
        use_rag = data.get('use_rag', RAG_ENABLED) and RAG_AVAILABLE
        selected_documents = data.get('selected_documents', [])  # List of doc IDs to use
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Create conversation if needed
        if conversation_id is None:
            title = user_message[:50] + "..." if len(user_message) > 50 else user_message
            conversation_id = db.create_conversation(title, DEFAULT_MODEL)
            CURRENT_CONVERSATION_ID = conversation_id
        
        print(f"\n👤 User (Conv {conversation_id}): {user_message}")
        if selected_documents:
            print(f"📄 Using documents: {selected_documents}")
        
        # Save user message
        db.save_message(conversation_id, 'user', user_message, has_rag=False)
        
        # Get conversation history for context (last 10 messages)
        conversation_history = db.get_conversation_messages(conversation_id)
        # Only get the last 10 messages to avoid token limits
        recent_history = conversation_history[-11:-1] if len(conversation_history) > 10 else conversation_history[:-1]
        
        # USE RAG ENGINE IF AVAILABLE
        if RAG_AVAILABLE and use_rag:
            print("🔍 Using RAG engine...")
            rag_result = rag_engine.chat_with_rag(
                query=user_message,
                model=DEFAULT_MODEL,
                use_rag=use_rag,
                top_k=3,
                conversation_history=recent_history,
                selected_doc_ids=selected_documents  # Pass selected documents
            )
            ai_response = rag_result['response']
            has_context = rag_result['has_rag_context']
            sources = rag_result.get('sources', [])
        else:
            # Standard chat without RAG - build conversation context
            print("💬 Standard chat (RAG not available)...")
            
            # Build conversation history context
            history_text = ""
            if recent_history:
                history_text = "\n\nPrevious conversation:\n"
                for msg in recent_history:
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    history_text += f"{role}: {msg['content']}\n"
            
            # Add system identity with conversation history
            system_prompt = f"""You are a helpful AI assistant. Your name is "Offline AI Chatbot with RAG". You are an offline, privacy-focused conversational AI system.

IDENTITY GUIDELINES:
- Only mention your name or introduce yourself when specifically asked about your identity, name, or who you are
- For all other questions, just answer naturally without mentioning your name
- You run completely offline using Ollama for privacy and security
{history_text}
User's current message: {user_message}

Your response:"""
            
            payload = {
                "model": DEFAULT_MODEL,
                "prompt": system_prompt,
                "stream": False
            }
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
            if response.status_code == 200:
                ai_response = response.json().get('response', 'Sorry, I could not generate a response.')
            else:
                ai_response = 'Sorry, the AI is having trouble right now.'
            has_context = False
            sources = []
        
        print(f"🤖 AI: {ai_response[:100]}...")
        
        # Save response
        db.save_message(conversation_id, 'assistant', ai_response, has_rag=has_context)
        
        return jsonify({
            'response': ai_response,
            'model': DEFAULT_MODEL,
            'conversation_id': conversation_id,
            'has_rag_context': has_context,
            'sources': sources
        })
            
    except requests.exceptions.ConnectionError:
        error_msg = '⚠️ Cannot connect to Ollama! Make sure Ollama is running.'
        if conversation_id:
            db.save_message(conversation_id, 'assistant', error_msg, has_rag=False)
        return jsonify({'error': 'Cannot connect to Ollama', 'response': error_msg, 'conversation_id': conversation_id}), 500
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        error_msg = f'An error occurred: {str(e)}'
        if conversation_id:
            try:
                db.save_message(conversation_id, 'assistant', error_msg, has_rag=False)
            except:
                pass
        return jsonify({'error': str(e), 'response': error_msg, 'conversation_id': conversation_id}), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint - just to verify the server is running.
    Visit http://localhost:5000/health in your browser to test it.
    """
    try:
        # Try to connect to Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            return jsonify({
                'status': 'healthy',
                'ollama': 'connected',
                'available_models': model_names
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'ollama': 'not responding'
            }), 503
    except:
        return jsonify({
            'status': 'unhealthy',
            'ollama': 'not connected',
            'message': 'Make sure Ollama is running!'
        }), 503


@app.route('/api/models', methods=['GET'])
def get_models():
    """
    Get list of available models from Ollama
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return jsonify({
                'status': 'success',
                'models': models,
                'current_model': DEFAULT_MODEL
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Could not fetch models'
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/models/active', methods=['GET', 'POST'])
def active_model():
    """
    Get or set the active model
    """
    global DEFAULT_MODEL
    
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'model': DEFAULT_MODEL
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        new_model = data.get('model', '')
        
        if not new_model:
            return jsonify({
                'status': 'error',
                'message': 'No model specified'
            }), 400
        
        # Update the active model
        DEFAULT_MODEL = new_model
        return jsonify({
            'status': 'success',
            'model': DEFAULT_MODEL,
            'message': f'Active model changed to {new_model}'
        })


@app.route('/api/models/download', methods=['POST'])
def download_model():
    """
    Download a new model from Ollama
    """
    try:
        data = request.get_json()
        model_name = data.get('model', '')
        
        if not model_name:
            return jsonify({
                'status': 'error',
                'message': 'No model specified'
            }), 400
        
        # Trigger model download
        # Note: This is a non-blocking call. The actual download happens in background
        response = requests.post(
            "http://localhost:11434/api/pull",
            json={"name": model_name},
            timeout=10
        )
        
        if response.status_code == 200:
            return jsonify({
                'status': 'success',
                'message': f'Started downloading {model_name}'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to start download'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ==========================================
# CONVERSATION MANAGEMENT ENDPOINTS
# ==========================================

@app.route('/api/conversations/new', methods=['POST'])
def new_conversation():
    """Create a new conversation"""
    global CURRENT_CONVERSATION_ID
    
    try:
        data = request.get_json() or {}
        title = data.get('title', 'New Chat')
        model = data.get('model', DEFAULT_MODEL)
        
        conversation_id = db.create_conversation(title, model)
        CURRENT_CONVERSATION_ID = conversation_id
        
        return jsonify({
            'status': 'success',
            'conversation_id': conversation_id,
            'title': title
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """Get list of all conversations"""
    try:
        conversations = db.get_all_conversations()
        return jsonify({
            'status': 'success',
            'conversations': conversations
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
        

@app.route('/api/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get specific conversation with all messages"""
    try:
        conversation = db.get_conversation(conversation_id)
        
        if not conversation:
            return jsonify({
                'status': 'error',
                'message': 'Conversation not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'conversation': conversation
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation_endpoint(conversation_id):
    """Delete a conversation"""
    global CURRENT_CONVERSATION_ID
    
    try:
        db.delete_conversation(conversation_id)
        
        # Clear current conversation if it was deleted
        if CURRENT_CONVERSATION_ID == conversation_id:
            CURRENT_CONVERSATION_ID = None
        
        return jsonify({
            'status': 'success',
            'message': 'Conversation deleted'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/conversations/<int:conversation_id>/set-active', methods=['POST'])
def set_active_conversation(conversation_id):
    """Set the active conversation"""
    global CURRENT_CONVERSATION_ID
    
    try:
        # Verify conversation exists
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            return jsonify({
                'status': 'error',
                'message': 'Conversation not found'
            }), 404
        
        CURRENT_CONVERSATION_ID = conversation_id
        
        return jsonify({
            'status': 'success',
            'conversation_id': conversation_id
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ==========================================
# DOCUMENT MANAGEMENT ENDPOINTS
# ==========================================

@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    """Upload and process a PDF document"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'status': 'error', 'message': 'Only PDF files are allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        import time
        timestamp = str(int(time.time()))
        safe_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        print(f"📄 Uploaded: {filename} ({file_size} bytes)")
        
        # Process PDF
        result = pdf_processor.process_pdf(file_path)
        
        # Add to database
        doc_id = db.add_document(
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            page_count=result['page_count']
        )
        
        # Add to vector store
        vector_store.add_document(
            doc_id=doc_id,
            chunks=result['chunks'],
            metadata={'filename': filename}
        )
        
        # Update status
        db.update_document_status(doc_id, 'ready')
        
        # Auto-generate summary in background (use first chunks as context)
        try:
            summary = _generate_doc_summary(doc_id, filename)
            if summary:
                db.save_document_summary(doc_id, summary)
                print(f"📝 Summary generated for doc {doc_id}")
        except Exception as e:
            print(f"⚠️ Summary generation failed: {e}")
        
        print(f"✅ Document {doc_id} processed successfully")
        
        return jsonify({
            'status': 'success',
            'document_id': doc_id,
            'filename': filename,
            'pages': result['page_count'],
            'chunks': result['chunk_count'],
            'summary': db.get_document_summary(doc_id)
        })
        
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/documents', methods=['GET'])
def list_documents():
    """Get list of all uploaded documents"""
    try:
        documents = db.get_documents()
        return jsonify({
            'status': 'success',
            'documents': documents
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
def delete_document_endpoint(doc_id):
    """Delete a document"""
    try:
        # Get document info
        doc = db.get_document_by_id(doc_id)
        if not doc:
            return jsonify({'status': 'error', 'message': 'Document not found'}), 404
        
        # Delete from vector store
        vector_store.delete_document(doc_id)
        
        # Delete file
        if os.path.exists(doc['file_path']):
            os.remove(doc['file_path'])
        
        # Delete from database
        db.delete_document(doc_id)
        
        print(f"✅ Deleted document {doc_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Document deleted'
        })
    except Exception as e:
        print(f"❌ Delete error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ==========================================
# STUDY ASSISTANT HELPER
# ==========================================

def _get_doc_text_chunks(doc_id: int, top_k: int = 8) -> str:
    """Retrieve top chunks from a document as a single text block for prompts."""
    if not RAG_AVAILABLE:
        return ""
    chunks = rag_engine.retrieve_context_from_docs(
        query="summarize key topics information content",
        doc_ids=[doc_id],
        top_k=top_k
    )
    if not chunks:
        return ""
    return "\n\n".join([c['text'] for c in chunks])


def _generate_doc_summary(doc_id: int, filename: str) -> str:
    """Generate a 3-line summary for a document using Ollama."""
    context = _get_doc_text_chunks(doc_id, top_k=5)
    if not context:
        return None
    prompt = f"""You are a helpful academic assistant. Based on the following excerpt from a PDF document called '{filename}', write a concise 2-3 sentence summary that describes what the document is about. Be specific. Do NOT use bullet points — write in plain sentences only.

Document excerpt:
{context}

Summary:"""
    try:
        payload = {"model": DEFAULT_MODEL, "prompt": prompt, "stream": False}
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get('response', '').strip()
    except Exception as e:
        print(f"Summary Ollama error: {e}")
    return None


# ==========================================
# STUDY ASSISTANT ENDPOINTS
# ==========================================

@app.route('/api/documents/<int:doc_id>/summary', methods=['POST'])
def regenerate_summary(doc_id):
    """Re-generate and return summary for a document"""
    try:
        doc = db.get_document_by_id(doc_id)
        if not doc:
            return jsonify({'status': 'error', 'message': 'Document not found'}), 404
        summary = _generate_doc_summary(doc_id, doc['filename'])
        if summary:
            db.save_document_summary(doc_id, summary)
        return jsonify({'status': 'success', 'summary': summary or 'Could not generate summary.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/documents/<int:doc_id>/quiz', methods=['POST'])
def generate_quiz(doc_id):
    """Generate 5 MCQ questions from a document"""
    try:
        doc = db.get_document_by_id(doc_id)
        if not doc:
            return jsonify({'status': 'error', 'message': 'Document not found'}), 404
        # Get ALL chunks from the document directly (not limited by similarity)
        all_chunk_texts = []
        for i, meta in enumerate(rag_engine.vector_store.metadata):
            if meta['doc_id'] == doc_id:
                all_chunk_texts.append(rag_engine.vector_store.documents[i])

        if not all_chunk_texts:
            # fallback to similarity search
            chunks = rag_engine.retrieve_context_from_docs(
                query="main topics concepts definitions",
                doc_ids=[doc_id],
                top_k=10
            )
            all_chunk_texts = [c['text'] for c in chunks]

        if not all_chunk_texts:
            return jsonify({'status': 'error', 'message': 'No content found. Please re-upload the PDF.'}), 400

        context = "\n\n".join(all_chunk_texts[:12])  # Use up to 12 chunks

        prompt = f"""You are a quiz generator. Read the document excerpt and generate 5 multiple-choice questions.

Use EXACTLY this format for each question:

Q: [question text here]
A) [option text]
B) [option text]
C) [option text]
D) [option text]
ANSWER: [A or B or C or D]

Put one blank line between questions. Do not add numbering or any other text.

Document excerpt:
{context}

Questions:"""

        payload = {{"model": DEFAULT_MODEL, "prompt": prompt, "stream": False}}
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        if response.status_code != 200:
            return jsonify({{'status': 'error', 'message': 'AI generation failed'}}), 500

        raw = response.json().get('response', '').strip()
        print(f"[QUIZ RAW]:\n{{raw[:500]}}")

        # Robust line-by-line parser
        questions = []
        q_obj = {{}}
        options = {{}}

        for line in raw.splitlines():
            line = line.strip()
            if not line:
                if q_obj.get('question') and len(options) >= 2 and q_obj.get('answer'):
                    q_obj['options'] = options
                    questions.append(q_obj)
                    q_obj = {{}}
                    options = {{}}
                continue

            upper = line.upper()
            if upper.startswith('Q:') or upper.startswith('Q.'):
                if q_obj.get('question') and len(options) >= 2 and q_obj.get('answer'):
                    q_obj['options'] = options
                    questions.append(q_obj)
                q_obj = {{'question': line[2:].strip()}}
                options = {{}}
            elif upper.startswith('A)') or upper.startswith('A.') or upper.startswith('(A)'):
                options['A'] = line[2:].strip().lstrip('.) ')
            elif upper.startswith('B)') or upper.startswith('B.') or upper.startswith('(B)'):
                options['B'] = line[2:].strip().lstrip('.) ')
            elif upper.startswith('C)') or upper.startswith('C.') or upper.startswith('(C)'):
                options['C'] = line[2:].strip().lstrip('.) ')
            elif upper.startswith('D)') or upper.startswith('D.') or upper.startswith('(D)'):
                options['D'] = line[2:].strip().lstrip('.) ')
            elif upper.startswith('ANSWER:') or upper.startswith('CORRECT:'):
                ans = line.split(':', 1)[1].strip().upper()
                q_obj['answer'] = ans[0] if ans and ans[0] in 'ABCD' else 'A'

        # Final question
        if q_obj.get('question') and len(options) >= 2 and q_obj.get('answer'):
            q_obj['options'] = options
            questions.append(q_obj)

        questions = questions[:5]
        print(f"[QUIZ] Parsed {{len(questions)}} questions")
        return jsonify({{'status': 'success', 'document': doc['filename'], 'questions': questions}})
    except Exception as e:
        print(f"❌ Quiz error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/documents/<int:doc_id>/flashcards', methods=['POST'])
def generate_flashcards(doc_id):
    """Generate 8 flashcard pairs from a document"""
    try:
        doc = db.get_document_by_id(doc_id)
        if not doc:
            return jsonify({'status': 'error', 'message': 'Document not found'}), 404
        context = _get_doc_text_chunks(doc_id, top_k=8)
        if not context:
            return jsonify({'status': 'error', 'message': 'No content found in document'}), 400
        prompt = f"""You are an academic flashcard generator. Based on the document excerpt below, generate exactly 8 flashcards. 

For each flashcard use EXACTLY this format:
TERM: [key term or concept]
DEFINITION: [clear, concise explanation in 1-2 sentences]

Separate each flashcard with a blank line. Do not add numbering, headers, or any other text.

Document excerpt:
{context}

Flashcards:"""
        payload = {"model": DEFAULT_MODEL, "prompt": prompt, "stream": False}
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        if response.status_code != 200:
            return jsonify({'status': 'error', 'message': 'AI generation failed'}), 500
        raw = response.json().get('response', '').strip()
        # Parse flashcards
        flashcards = []
        blocks = [b.strip() for b in raw.split('\n\n') if b.strip()]
        for block in blocks:
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            card = {}
            for line in lines:
                if line.startswith('TERM:'):
                    card['term'] = line[5:].strip()
                elif line.startswith('DEFINITION:'):
                    card['definition'] = line[11:].strip()
            if card.get('term') and card.get('definition'):
                flashcards.append(card)
            if len(flashcards) >= 8:
                break
        return jsonify({'status': 'success', 'document': doc['filename'], 'flashcards': flashcards})
    except Exception as e:
        print(f"❌ Flashcard error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """
    Home page - just shows info about the API
    """
    return """
    <h1>🤖 AI Chatbot Backend</h1>
    <p>The server is running!</p>
    <ul>
        <li><a href="/health">Health Check</a> - Check if everything is working</li>
        <li>POST to /chat - Send messages to the AI</li>
    </ul>
    <p>Now open the <code>frontend/index.html</code> file in your browser to start chatting!</p>
    """


# Start the server
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║          🤖 AI CHATBOT BACKEND SERVER 🤖            ║
    ╚══════════════════════════════════════════════════════╝
    
    ✅ Server is starting...
    
    📍 Server will run at: http://localhost:5000
    🔧 Health check: http://localhost:5000/health
    💬 Chat endpoint: http://localhost:5000/chat
    
    ⚠️  IMPORTANT: Keep this window open!
    The chatbot won't work if you close this window.
    
    🌐 Now open frontend/index.html in your browser to start chatting!
    
    Press CTRL+C to stop the server.
    """)
    
    # Run the Flask app
    # - host='0.0.0.0' means it can be accessed from other devices on your network
    # - port=5000 is the port number (you can change this if needed)
    # - debug=True shows helpful error messages (turn off in production)
    app.run(host='0.0.0.0', port=5000, debug=True)
