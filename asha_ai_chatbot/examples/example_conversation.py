#!/usr/bin/env python3
"""
Example script demonstrating how to use the Asha Chatbot with the Groq API
"""

import sys
import os
import time

# Add the parent directory to the sys.path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_client import GroqAPIClient

def animate_typing(text, delay=0.03):
    """Create a typing animation effect for the chatbot responses"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def interactive_chat():
    """Run an interactive chat session with the Asha Chatbot"""
    print("\n========================================")
    print("   ASHA CHATBOT - INTERACTIVE MODE")
    print("========================================")
    print("Type 'exit', 'quit', or 'bye' to end the conversation")
    print("========================================\n")
    
    # Initialize the API client
    api_key = os.getenv("GROQ_API_KEY", "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")
    client = GroqAPIClient(api_key=api_key)
    
    # Initial system message to set the context
    system_message = """
    You are Asha, an AI career assistant designed to help women explore career opportunities,
    job listings, professional development events, and mentorship programs. 
    You provide supportive, encouraging, and bias-free guidance.
    Keep responses concise and focused on empowering women in their careers.
    """
    
    # Welcome message
    welcome_msg = "Hello! I'm Asha, your career assistant. How can I help with your professional journey today?"
    print("Asha: ", end="")
    animate_typing(welcome_msg)
    print()
    
    conversation_history = [
        {"role": "system", "content": system_message}
    ]
    
    # Main conversation loop
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\nAsha: Thank you for chatting with me today! Wishing you success in your career journey.")
            break
        
        if not user_input:
            continue
        
        # Add user message to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            print("Asha: ", end="")
            
            # Show typing indicator
            sys.stdout.flush()
            
            # Get response from API
            response = client.chat_completion(conversation_history)
            
            # Extract and display the assistant's response
            if response and "choices" in response and len(response["choices"]) > 0:
                assistant_response = response["choices"][0]["message"]["content"]
                animate_typing(assistant_response)
                
                # Add assistant response to conversation history
                conversation_history.append({"role": "assistant", "content": assistant_response})
            else:
                animate_typing("I'm sorry, I couldn't process your request.")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            animate_typing("I apologize, but I encountered an error. Let's try again.")

def demo_conversation():
    """Run a predefined demo conversation with the Asha Chatbot"""
    print("\n========================================")
    print("   ASHA CHATBOT - DEMO CONVERSATION")
    print("========================================\n")
    
    # Initialize the API client
    client = GroqAPIClient()
    
    # Predefined conversation
    conversation = [
        "Hello! I'm looking to transition from marketing to a tech role. Where should I start?",
        "What skills are most in-demand for women in tech right now?",
        "Can you recommend any women-focused mentorship programs in the tech industry?",
        "How should I prepare for my first technical interview?"
    ]
    
    try:
        for message in conversation:
            print(f"User: {message}")
            print("Asha: ", end="")
            response = client.simple_chat(message)
            animate_typing(response)
            print()
            time.sleep(1)  # Pause between exchanges
            
        print("\n=== Demo conversation completed ===\n")
        
    except Exception as e:
        print(f"\nError during demo: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Asha Chatbot Example")
    parser.add_argument("--demo", action="store_true", help="Run a demo conversation")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    if args.demo:
        demo_conversation()
    elif args.interactive:
        interactive_chat()
    else:
        # Default to interactive mode if no arguments provided
        interactive_chat() 