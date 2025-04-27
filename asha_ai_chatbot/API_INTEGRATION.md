# Asha Chatbot API Integration

This document explains how to use the Groq API integration with the Asha Chatbot.

## Overview

Asha Chatbot now includes integration with the Groq API, which provides access to powerful language models like Llama 3. This allows the chatbot to generate more natural, context-aware responses to user queries about career opportunities, job listings, mentorship, and professional development.

## API Key Setup

The API key is required to access Groq's services. There are several ways to set up your API key:

### Option 1: Environment Variable

Set the `GROQ_API_KEY` environment variable:

```bash
# Linux/Mac
export GROQ_API_KEY="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"

# Windows Command Prompt
set GROQ_API_KEY=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

# Windows PowerShell
$env:GROQ_API_KEY = "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"
```

### Option 2: .env File

Create a `.env` file in the project root directory with the following content:

```
GROQ_API_KEY=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
```

The application uses the `python-dotenv` package to load this file automatically.

### Option 3: Direct Initialization

You can also pass the API key directly when initializing the API client:

```python
from src.api_client import GroqAPIClient

client = GroqAPIClient(api_key="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")
```

## Usage Examples

### Basic Example

```python
from src.api_client import GroqAPIClient

# Initialize the client
client = GroqAPIClient()

# Get a response to a user message
response = client.simple_chat("I'm looking for career advice in the tech industry.")
print(response)
```

### Advanced Example with System Message

```python
from src.api_client import GroqAPIClient

# Initialize the client
client = GroqAPIClient()

# Create a system message to set context
system_message = "You are Asha, a career assistant specializing in tech careers."

# Get a response with the custom system message
response = client.simple_chat(
    "What skills should I focus on for a data science career?",
    system_message=system_message
)
print(response)
```

### Using with the Asha Chatbot Class

```python
from src.main import AshaAIBot

# Initialize the chatbot
asha = AshaAIBot()

# Generate a response using the API
response = asha.generate_response("How can I improve my resume for tech jobs?", use_api=True)

# Print the response
print(response["message"])
```

## Command-line Interface

The project includes a command-line interface for testing and interacting with the chatbot:

```bash
# Run with default settings (API with local fallback)
python cli.py

# Force API-only mode
python cli.py --api

# Force local-only mode
python cli.py --local

# Test the API connection directly
python cli.py --test-api
```

## API Response Format

When using the `chat_completion` method directly, the response will be in the standard Groq API format:

```json
{
  "id": "...",
  "object": "chat.completion",
  "created": 1619415426,
  "model": "llama3-70b-8192",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "The response content from the AI..."
      },
      "index": 0,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 56,
    "completion_tokens": 31,
    "total_tokens": 87
  }
}
```

When using the `simple_chat` method, you'll receive just the text content of the response.

## Error Handling

The API client includes error handling to manage common issues:

1. Invalid API key errors
2. Network connection problems
3. Rate limiting
4. Malformed requests

Errors are logged using the standard Python logging module and can be caught using try/except blocks.

## Customization

You can customize the API calls by modifying parameters:

```python
# Change the model
response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    model="llama3-8b-8192",  # Using a smaller model
    temperature=0.5,  # Lower temperature for more focused responses
    max_tokens=200    # Limit response length
)
```

## Security Considerations

- Never hardcode your API key directly in your application code
- Keep your API key secure and restrict access to it
- Consider using environment variables for production deployments
- Set appropriate rate limits to control API usage

## Troubleshooting

If you encounter issues with the API integration, try the following steps:

1. Verify your API key is correct and properly set
2. Check your internet connection
3. Run the API test: `python cli.py --test-api`
4. Check the logs for detailed error messages
5. Ensure you have the required dependencies installed 