#!/usr/bin/env python3
"""
Command-line interface for Asha Chatbot
Allows interaction with the chatbot from the terminal
"""

import os
import sys
import time
import argparse
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

# Make sure we can import from the current directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.main import AshaAIBot
    from src.api_client import GroqAPIClient
except ImportError as e:
    logger.error(f"Error importing required modules: {str(e)}")
    print(f"Error: {str(e)}")
    print("Make sure you're running this from the project root directory.")
    sys.exit(1)

def print_with_typing(text, delay=0.03):
    """Print text with a typing animation effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_divider():
    """Print a divider line"""
    print("\n" + "=" * 50 + "\n")

def run_interactive_session(api_only=False, local_only=False):
    """
    Run an interactive CLI session with the Asha Chatbot
    
    Args:
        api_only (bool): Only use API responses
        local_only (bool): Only use local responses
    """
    # Initialize the chatbot
    try:
        asha = AshaAIBot()
    except Exception as e:
        logger.error(f"Failed to initialize Asha Chatbot: {str(e)}")
        print(f"Error initializing chatbot: {str(e)}")
        return
        
    # Print welcome message
    print_divider()
    print("   ASHA CHATBOT - COMMAND LINE INTERFACE   ")
    print_divider()
    print("Type 'exit', 'quit', or 'bye' to end the session")
    print("Type '/api' to switch to API-only mode")
    print("Type '/local' to switch to local-only mode")
    print("Type '/auto' to switch to automatic mode (default)")
    print("Type '/clear' to clear the conversation history")
    print_divider()
    
    # Current mode
    use_api = not local_only
    
    # Welcome message
    print("Asha: ", end="")
    print_with_typing("Hello! I'm Asha, your career assistant. How can I help with your professional journey today?")
    
    # Main interaction loop
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for special commands
        if user_input.lower() in ['exit', 'quit', 'bye', '/exit', '/quit']:
            print("\nAsha: Thank you for chatting with me. Goodbye!")
            break
            
        elif user_input.lower() == '/api':
            use_api = True
            api_only = True
            local_only = False
            print("\nAsha: Switched to API-only mode. All responses will come from the Groq API.")
            continue
            
        elif user_input.lower() == '/local':
            use_api = False
            api_only = False
            local_only = True
            print("\nAsha: Switched to local-only mode. All responses will be generated locally.")
            continue
            
        elif user_input.lower() == '/auto':
            use_api = True
            api_only = False
            local_only = False
            print("\nAsha: Switched to automatic mode. Will try API first, then fall back to local responses if needed.")
            continue
            
        elif user_input.lower() == '/clear':
            asha.clear_conversation()
            print("\nAsha: Conversation history cleared.")
            continue
            
        if not user_input:
            continue
            
        # Generate response
        print("\nAsha is thinking...", end="\r")
        
        try:
            # Get response from chatbot
            response = asha.generate_response(user_input, use_api=use_api)
            
            # Clear the "thinking" message
            print(" " * 25, end="\r")
            
            # Print response with source indication
            source = response.get("source", "unknown")
            source_indicator = ""
            
            if api_only or local_only:
                if source == "groq_api":
                    source_indicator = " [API]"
                elif source in ["template", "rag", "default"]:
                    source_indicator = " [Local]"
            
            print(f"Asha{source_indicator}: ", end="")
            print_with_typing(response["message"])
            
        except Exception as e:
            logger.error(f"Error in conversation: {str(e)}")
            print(f"\nError: {str(e)}")
            print("Asha: I apologize, but I encountered an error. Let's try again.")

def test_api_directly():
    """Test the Groq API directly with a simple conversation"""
    api_key = os.getenv("GROQ_API_KEY", "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")
    
    # Initialize the API client
    try:
        client = GroqAPIClient(api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to initialize API client: {str(e)}")
        print(f"Error initializing API client: {str(e)}")
        return
    
    print_divider()
    print("   TESTING GROQ API CONNECTION   ")
    print_divider()
    
    # Test message
    test_message = "Hello, I'm looking for career advice in the tech industry."
    
    print(f"Sending test message to API: '{test_message}'")
    print("Waiting for response...")
    
    try:
        # Make the API call
        response = client.simple_chat(test_message)
        
        print_divider()
        print("API RESPONSE:")
        print_divider()
        print(response)
        print_divider()
        
        print("API test completed successfully!")
        
    except Exception as e:
        logger.error(f"API test failed: {str(e)}")
        print(f"Error testing API: {str(e)}")

def main():
    """Main entry point for the CLI application"""
    parser = argparse.ArgumentParser(description="Asha Chatbot CLI")
    
    # Add arguments
    parser.add_argument("--api", action="store_true", help="Use only API responses")
    parser.add_argument("--local", action="store_true", help="Use only local responses")
    parser.add_argument("--test-api", action="store_true", help="Test the API connection directly")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check for conflicting arguments
    if args.api and args.local:
        print("Error: Cannot specify both --api and --local")
        sys.exit(1)
    
    # Run in the appropriate mode
    if args.test_api:
        test_api_directly()
    else:
        run_interactive_session(api_only=args.api, local_only=args.local)

if __name__ == "__main__":
    main() 