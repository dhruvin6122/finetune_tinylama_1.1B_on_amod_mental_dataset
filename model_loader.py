"""
Model loader for Mental Health Assistant chatbot.
Loads the Hugging Face model and wraps it with LangChain.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import torch

# Model configuration
MODEL_NAME = "dhruvin0612/mental_health_assistant_1.1B"
SYSTEM_INSTRUCTION = """You are a mental health support assistant trained on mental health conversations. 

Respond in simple, easy-to-understand language like you're talking to a friend. Keep answers short and natural (1-3 sentences).

Your approach:
- Be warm and understanding
- Use everyday words, not medical terms
- Share simple coping tips when helpful
- Suggest talking to a professional if needed
- Never diagnose or give medical advice

You're here to listen and support, not to replace therapy."""

# Global variables for caching
_llm = None
_tokenizer = None


def load_model():
    """
    Load the Hugging Face model.
    This function caches the model to avoid reloading.
    """
    global _llm, _tokenizer
    
    if _llm is not None:
        print("Using cached model...")
        return _llm
    
    print(f"Loading model: {MODEL_NAME}")
    
    try:
        # Detect device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        # Load tokenizer and model
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None,
        )
        
        if device == "cpu":
            model = model.to(device)
        
        # Create pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=_tokenizer,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
        )
        
        # Wrap with LangChain
        _llm = HuggingFacePipeline(pipeline=pipe)
        
        print("✓ Model loaded successfully!")
        return _llm
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def get_response(llm, user_message, conversation_history=None):
    """
    Generate a response from the model given a user message and conversation history.
    
    Args:
        llm: The HuggingFacePipeline instance
        user_message: The user's message
        conversation_history: List of previous exchanges (optional)
    
    Returns:
        str: The assistant's response
    """
    # Build conversation prompt
    prompt = f"{SYSTEM_INSTRUCTION}\n\n"
    
    if conversation_history:
        for exchange in conversation_history:
            prompt += f"User: {exchange['user']}\n"
            prompt += f"Assistant: {exchange['assistant']}\n\n"
    
    # Add current user message
    prompt += f"User: {user_message}\n"
    prompt += "Assistant:"
    
    # Generate response
    try:
        response = llm.invoke(prompt)
        # Extract just the assistant's response
        assistant_response = response.split("Assistant:")[-1].strip()
        # Clean up if there's a next "User:" in the response
        if "User:" in assistant_response:
            assistant_response = assistant_response.split("User:")[0].strip()
        return assistant_response
    
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I apologize, but I'm having trouble generating a response right now. Please try again."


def get_response_stream(llm, user_message, conversation_history=None):
    """
    Generate a streaming response from the model.
    
    Args:
        llm: The HuggingFacePipeline instance
        user_message: The user's message
        conversation_history: List of previous exchanges (optional)
    
    Yields:
        str: Chunks of the assistant's response
    """
    # Build conversation prompt
    prompt = f"{SYSTEM_INSTRUCTION}\n\n"
    
    if conversation_history:
        for exchange in conversation_history:
            prompt += f"User: {exchange['user']}\n"
            prompt += f"Assistant: {exchange['assistant']}\n\n"
    
    # Add current user message
    prompt += f"User: {user_message}\n"
    prompt += "Assistant:"
    
    # Generate streaming response
    try:
        # Note: HuggingFace pipeline doesn't support true streaming
        # This is a workaround that yields the full response
        response = llm.invoke(prompt)
        assistant_response = response.split("Assistant:")[-1].strip()
        if "User:" in assistant_response:
            assistant_response = assistant_response.split("User:")[0].strip()
        
        # Simulate streaming by yielding word by word
        words = assistant_response.split()
        for i, word in enumerate(words):
            if i < len(words) - 1:
                yield word + " "
            else:
                yield word
    
    except Exception as e:
        print(f"Error generating streaming response: {e}")
        yield "I apologize, but I'm having trouble generating a response right now."
