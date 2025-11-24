# Mental Health Assistant Chatbot 🧠💙

A compassionate AI-powered mental health assistant built with your custom HuggingFace model, LangChain, and a beautiful modern UI.

## Features

✨ **Compassionate AI Support** - Uses your fine-tuned `dhruvin0612/mental_health_assistant_1.1B` model
🔗 **LangChain Integration** - Structured prompts and conversation management
🎨 **Premium UI** - Glassmorphic design with smooth animations
💬 **Conversation History** - Maintains context across messages
📱 **Responsive Design** - Works beautifully on mobile and desktop
⚡ **Real-time Responses** - Fast inference with typing indicators

## Technology Stack

- **Backend**: Python, Flask, LangChain
- **Model**: HuggingFace Transformers (`dhruvin0612/mental_health_assistant_1.1B`)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **UI Design**: Glassmorphism, CSS animations, responsive layout

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster inference

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd "c:\Users\kisha\Downloads\google antigravity projects\mental health assistant"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: First installation will download the model (~4.4GB). This may take several minutes depending on your internet connection.

## Usage

### Starting the Server

1. **Run the Flask application**
   ```bash
   python app.py
   ```

2. **Wait for model loading**
   - First run: Model will be downloaded from HuggingFace
   - Subsequent runs: Model loads from cache (much faster)

3. **Open your browser**
   - Navigate to: `http://localhost:5000`

### Using the Chatbot

1. Type your message in the input field
2. Press **Enter** or click the send button
3. Wait for the AI assistant's response
4. Continue the conversation naturally
5. Use **Clear Chat** to start a new conversation

### Keyboard Shortcuts

- `Enter` - Send message
- `Shift + Enter` - New line in message

## API Endpoints

### POST `/api/chat`
Send a message and receive AI response

**Request Body:**
```json
{
  "message": "I'm feeling anxious today",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "I hear you. Anxiety can be really challenging...",
  "session_id": "session_12345"
}
```

### POST `/api/clear`
Clear conversation history for a session

**Request Body:**
```json
{
  "session_id": "session_12345"
}
```

### GET `/api/health`
Check server and model status

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Project Structure

```
mental health assistant/
├── app.py                 # Flask server and API endpoints
├── model_loader.py        # Model loading and LangChain setup
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore patterns
├── README.md             # This file
└── static/               # Frontend files
    ├── index.html        # Main HTML structure
    ├── styles.css        # Premium UI styling
    └── script.js         # Chat functionality
```

## Configuration

### Model Parameters

Edit `model_loader.py` to adjust generation parameters:

```python
pipe = pipeline(
    "text-generation",
    model=_model,
    tokenizer=_tokenizer,
    max_new_tokens=512,      # Maximum response length
    temperature=0.7,         # Creativity (0.0-1.0)
    top_p=0.9,              # Nucleus sampling
    repetition_penalty=1.15, # Reduce repetition
    do_sample=True,
)
```

### System Instruction

Modify the system instruction in `model_loader.py`:

```python
SYSTEM_INSTRUCTION = """Your custom instruction here..."""
```

## Troubleshooting

### Model Loading Issues

**Problem**: Model fails to download
- **Solution**: Check internet connection and HuggingFace availability
- **Alternative**: Download model manually and place in cache directory

**Problem**: Out of memory error
- **Solution**: Reduce `max_new_tokens` or use CPU instead of GPU

### Server Issues

**Problem**: Port 5000 already in use
- **Solution**: Change port in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

**Problem**: CORS errors
- **Solution**: Ensure `flask-cors` is installed and CORS is enabled

### UI Issues

**Problem**: Chat not loading
- **Solution**: Check browser console for errors
- **Solution**: Ensure server is running on `http://localhost:5000`

## Performance Tips

1. **Use GPU**: If available, model will automatically use CUDA for faster inference
2. **Reduce max_new_tokens**: Shorter responses = faster generation
3. **Adjust temperature**: Lower values (0.5-0.7) generate faster
4. **Clear history**: Regularly clear conversation to reduce context size

## Disclaimer

⚠️ **Important**: This chatbot is designed to provide supportive conversations and coping strategies. It is **NOT** a replacement for professional mental health care, therapy, or medical advice.

If you or someone you know is experiencing a mental health crisis, please contact:
- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741 (US)
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

## License

This project uses the HuggingFace model `dhruvin0612/mental_health_assistant_1.1B`. Please refer to the model's license on HuggingFace for usage terms.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- Model: `dhruvin0612/mental_health_assistant_1.1B` from HuggingFace
- Framework: LangChain for prompt management
- UI Inspiration: Modern glassmorphic design principles

---

Built with ❤️ for mental health support
