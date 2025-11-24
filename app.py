"""
Flask API server for Mental Health Assistant chatbot.
Provides REST API endpoints for chat inference.
"""

from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS
from model_loader import load_model, get_response_stream
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Store conversation history per session (in-memory)
conversations = {}

# Load model on startup
print("Initializing Mental Health Assistant...")
try:
    llm_chain = load_model()
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    llm_chain = None


@app.route('/')
def index():
    """Serve the main chat interface."""
    return send_from_directory('static', 'index.html')


@app.route('/styles.css')
def serve_css():
    """Serve the CSS file."""
    return send_from_directory('static', 'styles.css', mimetype='text/css')


@app.route('/script.js')
def serve_js():
    """Serve the JavaScript file."""
    return send_from_directory('static', 'script.js', mimetype='application/javascript')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages and return AI responses.
    
    Expected JSON payload:
    {
        "message": "user message",
        "session_id": "optional session identifier"
    }
    """
    try:
        if llm_chain is None:
            return jsonify({
                'error': 'Model not loaded. Please restart the server.'
            }), 503
        
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create conversation history
        if session_id not in conversations:
            conversations[session_id] = []
        
        history = conversations[session_id]
        
        def generate():
            full_response = ""
            for chunk in get_response_stream(llm_chain, user_message, history):
                full_response += chunk
                yield chunk
            
            # Update conversation history after stream completes
            history.append({
                'user': user_message,
                'assistant': full_response
            })
            
            # Keep only last 5 exchanges to manage memory
            if len(history) > 5:
                history.pop(0)

        return Response(stream_with_context(generate()), mimetype='text/plain')
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'An error occurred while processing your message. Please try again.'
        }), 500


@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history for a session."""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in conversations:
            conversations[session_id] = []
        
        return jsonify({'message': 'Conversation cleared'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': llm_chain is not None
    })


if __name__ == '__main__':
    print("\n" + "="*50)
    print("Mental Health Assistant Chatbot")
    print("="*50)
    print(f"Server starting on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
