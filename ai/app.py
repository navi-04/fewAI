from flask import Flask, request, jsonify, send_from_directory
import os
import time
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# API Keys (should be stored in environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# API Endpoints
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/"

# Model configurations
MODEL_CONFIG = {
    "gpt-4": {
        "provider": "openai",
        "model_name": "gpt-4",
        "max_tokens": 500
    },
    "gpt-3.5": {
        "provider": "openai",
        "model_name": "gpt-3.5-turbo",
        "max_tokens": 500
    },
    "claude": {
        "provider": "anthropic",
        "model_name": "claude-3-opus-20240229",
        "max_tokens": 500
    },
    "llama": {
        "provider": "huggingface",
        "model_name": "meta-llama/Llama-2-70b-chat-hf",
        "max_tokens": 500
    },
    "gemini": {
        "provider": "google",
        "model_name": "gemini-pro",
        "max_tokens": 500
    }
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

def call_openai_api(message, model_name, max_tokens):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": message}],
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return f"Error calling OpenAI API: {e}"

def call_anthropic_api(message, model_name, max_tokens):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": message}],
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
        response_data = response.json()
        return response_data["content"][0]["text"]
    except Exception as e:
        print(f"Anthropic API error: {e}")
        return f"Error calling Anthropic API: {e}"

def call_huggingface_api(message, model_name):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }
    
    data = {
        "inputs": message,
        "parameters": {
            "max_length": 500,
            "temperature": 0.7,
        }
    }
    
    try:
        api_url = f"{HUGGINGFACE_API_URL}{model_name}"
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()[0]["generated_text"]
    except Exception as e:
        print(f"Hugging Face API error: {e}")
        return f"Error calling Hugging Face API: {e}"

def get_ai_response(message, model):
    config = MODEL_CONFIG.get(model)
    if not config:
        return "Selected model is not available."
    
    provider = config["provider"]
    model_name = config["model_name"]
    max_tokens = config.get("max_tokens", 500)
    
    if provider == "openai":
        if not OPENAI_API_KEY:
            return "OpenAI API key is not configured."
        return call_openai_api(message, model_name, max_tokens)
    
    elif provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            return "Anthropic API key is not configured."
        return call_anthropic_api(message, model_name, max_tokens)
    
    elif provider == "huggingface":
        if not HUGGINGFACE_API_KEY:
            return "Hugging Face API key is not configured."
        return call_huggingface_api(message, model_name)
    
    elif provider == "google":
        return "Google Gemini API integration is not yet implemented."
    
    return "Unsupported AI provider."

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    model = data.get('model', 'gpt-4')
    
    # Get response from actual AI API
    response = get_ai_response(user_message, model)
    
    return jsonify({"response": response})

@app.route('/api/models', methods=['GET'])
def get_models():
    available_models = []
    for model, config in MODEL_CONFIG.items():
        api_key_env_var = f"{config['provider'].upper()}_API_KEY"
        api_key = os.getenv(api_key_env_var)
        available_models.append({
            "id": model,
            "name": model.upper(),
            "available": api_key is not None
        })
    
    return jsonify({"models": available_models})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)