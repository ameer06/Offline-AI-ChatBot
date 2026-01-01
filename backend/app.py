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

# Create the Flask app (this is your server)
app = Flask(__name__)

# Enable CORS - this allows your HTML page to talk to this server
# Without this, browsers block the connection for security reasons
CORS(app)

# Configuration - you can change these!
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Where Ollama is running
DEFAULT_MODEL = "llama3.2"  # Which AI model to use

# You can change the model here to try different ones:
# - "llama3.2" - Best all-around
# - "mistral" - Faster, good for slower computers  
# - "codellama" - Best for coding questions
# - "gemma:7b" - Google's model


@app.route('/chat', methods=['POST'])
def chat():
    """
    This is the main function that handles chat messages.
    
    When someone types a message on the website, it comes here.
    We then send it to Ollama and get a response.
    """
    
    try:
        # Get the message from the user
        # The frontend sends JSON data like: {"message": "Hello!"}
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Check if the message is empty
        if not user_message:
            return jsonify({
                'error': 'No message provided',
                'response': 'Please type a message!'
            }), 400
        
        print(f"\n👤 User: {user_message}")  # Print to console so you can see what's happening
        
        # Prepare the request to send to Ollama
        payload = {
            "model": DEFAULT_MODEL,      # Which AI model to use
            "prompt": user_message,      # The user's question
            "stream": False              # Get the complete response at once (not word-by-word)
        }
        
        # Send the request to Ollama
        print("🤔 Thinking...")
        response = requests.post(
            OLLAMA_API_URL, 
            json=payload,
            timeout=120  # Wait up to 2 minutes for a response
        )
        
        # Check if Ollama responded successfully
        if response.status_code == 200:
            # Get the AI's response
            ai_response = response.json().get('response', 'Sorry, I could not generate a response.')
            print(f"🤖 AI: {ai_response[:100]}...")  # Print first 100 characters
            
            # Send the response back to the frontend
            return jsonify({
                'response': ai_response,
                'model': DEFAULT_MODEL
            })
        else:
            # Something went wrong with Ollama
            return jsonify({
                'error': f'Ollama error: {response.status_code}',
                'response': 'Sorry, the AI is having trouble right now. Make sure Ollama is running!'
            }), 500
            
    except requests.exceptions.ConnectionError:
        # This happens when Ollama is not running
        return jsonify({
            'error': 'Cannot connect to Ollama',
            'response': '⚠️ Cannot connect to Ollama! Make sure:\n1. Ollama is installed\n2. Ollama is running\n3. You have downloaded a model (ollama pull llama3.2)'
        }), 500
        
    except requests.exceptions.Timeout:
        # This happens when the AI takes too long to respond
        return jsonify({
            'error': 'Request timeout',
            'response': '⏱️ The AI is taking too long to respond. Try a shorter message or restart Ollama.'
        }), 504
        
    except Exception as e:
        # Catch any other errors
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'error': str(e),
            'response': f'An error occurred: {str(e)}'
        }), 500


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
