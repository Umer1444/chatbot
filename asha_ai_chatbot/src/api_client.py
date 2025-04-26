"""
API Client for Asha Chatbot
Handles interactions with the Groq API 
"""

import os
import requests
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class GroqAPIClient:
    """Client for interacting with the Groq API"""
    
    def __init__(self, api_key=None):
        """
        Initialize the Groq API client
        
        Args:
            api_key (str, optional): API key for Groq. If not provided, will look for GROQ_API_KEY env variable
        """
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "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")
        
        if not self.api_key:
            logger.warning("No API key provided. API calls will fail.")
        
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        logger.info("Groq API client initialized")
    
    def chat_completion(self, messages, model="llama3-70b-8192", temperature=0.7, max_tokens=800):
        """
        Send a chat completion request to the Groq API
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            model (str): The model to use for completion
            temperature (float): Sampling temperature (0.0 to 1.0)
            max_tokens (int): Maximum number of tokens to generate
            
        Returns:
            dict: The API response
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        # Prepare request data
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            logger.info(f"Sending request to Groq API with model: {model}")
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            result = response.json()
            logger.info("Successfully received response from Groq API")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            raise
    
    def simple_chat(self, user_message, system_message=None):
        """
        Simplified method for sending a single message and getting a response
        
        Args:
            user_message (str): The user's message
            system_message (str, optional): System message to set context
            
        Returns:
            str: The assistant's response text
        """
        # Prepare messages
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})
        else:
            # Default system message for Asha
            messages.append({
                "role": "system", 
                "content": "You are Asha, an AI career assistant designed to help women explore career opportunities, "
                           "job listings, professional development events, and mentorship programs through natural "
                           "language conversations. Provide helpful, supportive, and bias-free responses."
            })
        
        # Add user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Send request
            response = self.chat_completion(messages)
            
            # Extract assistant's message
            if response and "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            else:
                logger.warning("Unexpected response format from API")
                return "I'm sorry, I couldn't process your request."
                
        except Exception as e:
            logger.error(f"Error in simple_chat: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"


def test_api_client():
    """Test the API client with a simple conversation"""
    client = GroqAPIClient()
    
    # Example conversation
    system_msg = "You are Asha, a helpful career assistant for women. Keep responses brief and supportive."
    user_messages = [
        "Hello, can you help me find job opportunities in tech?",
        "I have experience in Python programming. What roles should I look for?",
        "How should I prepare for a technical interview?"
    ]
    
    print("\n=== Testing Asha Chatbot API Client ===\n")
    
    try:
        for i, msg in enumerate(user_messages):
            print(f"User: {msg}")
            response = client.simple_chat(msg, system_message=system_msg if i == 0 else None)
            print(f"Asha: {response}\n")
    except Exception as e:
        print(f"Error during test: {str(e)}")


if __name__ == "__main__":
    # Run a simple test if this file is executed directly
    test_api_client() 