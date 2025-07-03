# Real AI Chat Assistant

A ChatGPT-like interface that connects to actual AI models through their APIs.

## Setup Instructions

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   ```

3. Start the Flask server:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Features

- Real AI responses from OpenAI, Anthropic, and Hugging Face models
- Multiple model selection
- Responsive chat interface

## Notes

- You need valid API keys for the services you want to use
- API usage will incur costs according to each provider's pricing
- For security, never share your API keys or commit them to public repositories
