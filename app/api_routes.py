"""
API Routes for Asha Chatbot
Handles all API endpoints for live conversation
"""

from flask import Blueprint, request, jsonify
import os
import requests
import logging
import uuid
import sys
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Blueprint for API routes
api = Blueprint('api', __name__)

# Dictionary to store active conversations
active_conversations = {}

@api.route('/chat', methods=['POST'])
def chat():
    """API endpoint that now redirects to live chat (local processing removed)"""
    try:
        data = request.json
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        return jsonify({
            "type": "error",
            "message": "Local processing is no longer supported. Please use the live chat with your API key instead.",
            "session_id": session_id
        }), 400
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "type": "error",
            "message": "I apologize, but I encountered an issue processing your request. Please try again.",
            "session_id": session_id if session_id else str(uuid.uuid4())
        }), 500

@api.route('/live_chat', methods=['POST'])
def live_chat():
    """API endpoint for live chatbot interaction with external API (Groq)"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', None)
        provider = data.get('provider', 'groq')
        user_api_key = data.get('api_key', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
            
        if not user_api_key:
            return jsonify({"error": "No API key provided. Please set your Groq API key in the settings."}), 400
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            # Initialize conversation history for new session
            active_conversations[session_id] = []
            
        # Ensure session exists in our tracking
        if session_id not in active_conversations:
            active_conversations[session_id] = []
            
        # Add user message to conversation history
        active_conversations[session_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Use user-provided API key
        api_key = user_api_key
        
        # System prompt that defines the assistant's behavior
        system_prompt = """
        You are Asha, an AI career assistant designed to help women explore career opportunities,
        job listings, professional development events, and mentorship programs. 
        You provide supportive, encouraging, and bias-free guidance.
        Keep responses concise and focused on empowering women in their careers.
        """
        
        # Prepare messages including history for context
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (up to last 10 messages)
        history = active_conversations[session_id][-10:] if len(active_conversations[session_id]) > 10 else active_conversations[session_id]
        messages.extend(history)
        
        if provider == 'groq' or provider == 'xai':
            # Use Groq API with LLaMA model
            try:
                response = requests.post(
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {api_key}'
                    },
                    json={
                        'messages': messages,
                        'model': 'llama3-70b-8192',
                        'temperature': 0.7,
                        'max_tokens': 800
                    },
                    timeout=30  # 30 second timeout
                )
                
                # Check response status
                response.raise_for_status()
                result = response.json()
                
                # Extract response content
                if result and 'choices' in result and len(result['choices']) > 0:
                    bot_message = result['choices'][0]['message']['content']
                    
                    # Add bot response to conversation history
                    active_conversations[session_id].append({
                        "role": "assistant",
                        "content": bot_message
                    })
                    
                    # Prepare the response
                    api_response = {
                        "message": bot_message,
                        "session_id": session_id,
                        "source": "groq_api",
                        "type": "normal"
                    }
                    
                    # Log success
                    logger.info(f"Successfully got response from Groq API for session {session_id[:8]}")
                    
                    return jsonify(api_response)
                else:
                    raise ValueError("Invalid response format from API")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"API request failed: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    error_msg = f"API error ({e.response.status_code}): {e.response.text if hasattr(e.response, 'text') else 'Unknown error'}"
                else:
                    error_msg = f"API request error: {str(e)}"
                return jsonify({"error": error_msg}), 400
                
            except Exception as e:
                logger.error(f"Error using Groq API: {str(e)}")
                return jsonify({"error": f"Error: {str(e)}"}), 400
                
        else:
            # Unsupported provider
            return jsonify({
                "error": f"Unsupported provider: {provider}. Only Groq/LLaMA models are supported."
            }), 400
            
    except Exception as e:
        logger.error(f"Error in live_chat endpoint: {str(e)}")
        return jsonify({
            "error": f"Error processing request: {str(e)}"
        }), 500

def fallback_to_local(user_message, session_id):
    """Error handler for API failures that returns a consistent error message"""
    logger.error(f"API request failed for session {session_id[:8]}")
    
    return jsonify({
        "error": "I apologize, but I cannot connect to the AI service at the moment. Please check your API key and try again.",
        "session_id": session_id,
        "source": "error",
        "type": "error"
    }), 400

@api.route('/clear_session', methods=['POST'])
def clear_session():
    """Clear conversation history for a specific session"""
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({"error": "No session_id provided"}), 400
        
    if session_id in active_conversations:
        active_conversations[session_id] = []
        
    return jsonify({"success": True, "message": "Session cleared"})

@api.route('/session_history', methods=['GET'])
def session_history():
    """Get conversation history for a specific session"""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return jsonify({"error": "No session_id provided"}), 400
        
    history = active_conversations.get(session_id, [])
    
    return jsonify({
        "session_id": session_id,
        "history": history,
        "message_count": len(history)
    }) 