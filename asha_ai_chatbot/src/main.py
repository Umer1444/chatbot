"""
Asha AI Chatbot - Main Module
Handles integration between API, UI, and business logic
"""

import logging
import os
from typing import Dict, List, Optional, Any, Union
from .rag_pipeline import RAGPipeline
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AshaAIBot:
    """
    Main class for the Asha AI Chatbot
    Handles integration between different components
    """
    
    def __init__(self):
        """Initialize the chatbot with necessary components"""
        try:
            # Initialize RAG pipeline for context-aware responses
            self.rag_pipeline = RAGPipeline()
            logger.info("Initialized RAG pipeline for context retrieval")
            
            # Set up Groq API integration
            self.groq_api_key = os.getenv("GROQ_API_KEY", "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")
            self.model = os.getenv("DEFAULT_MODEL", "llama3-70b-8192")
            self.api_enabled = True if self.groq_api_key else False
            
            if self.api_enabled:
                logger.info("Groq API integration enabled")
            else:
                logger.warning("Groq API integration disabled - no API key found")
                
            self.conversation_history = {}
            
        except Exception as e:
            logger.error(f"Error initializing AshaAIBot: {str(e)}")
            raise
    
    def process_query(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process a user query through the Asha Chatbot (main interface method)
        
        Args:
            query (str): The user's query text
            session_id (str, optional): Session identifier for conversation tracking
            
        Returns:
            dict: Response containing message and metadata
        """
        # Generate a session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            
        logger.info(f"Processing query for session {session_id}: {query[:50]}...")
        
        try:
            # Generate response to the query
            response = self.generate_response(query, use_api=True, session_id=session_id)
            
            # Return formatted response for the web interface
            return {
                "message": response["message"],
                "type": "normal",
                "session_id": session_id,
                "source": response.get("source", "default")
            }
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "message": "I apologize, but I encountered an issue processing your request. Please try again.",
                "type": "error",
                "session_id": session_id,
                "source": "error"
            }
    
    def generate_response(self, user_message: str, use_api: bool = True, session_id: str = None) -> Dict[str, Any]:
        """
        Generate a response to the user's message
        
        Args:
            user_message (str): The user's message
            use_api (bool): Whether to use the Groq API or fallback to local methods
            session_id (str, optional): Session identifier for conversation tracking
            
        Returns:
            dict: Response containing the message and metadata
        """
        logger.info(f"Generating response for user message: {user_message[:50]}...")
        
        # Use default session ID if not provided
        if not session_id:
            session_id = "default"
            
        # Initialize conversation history for this session if it doesn't exist
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        # Track conversation for context
        self.conversation_history[session_id].append({"role": "user", "content": user_message})
        
        try:
            # Use API if enabled and requested
            if self.api_enabled and use_api:
                logger.info("Using Groq API for response generation")
                response = self._generate_api_response(user_message, session_id)
            else:
                logger.info("Using local response generation")
                response = self._generate_local_response(user_message)
                
            # Add response to conversation history
            self.conversation_history[session_id].append({"role": "assistant", "content": response["message"]})
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            error_response = {
                "message": f"I apologize, but I encountered an error: {str(e)}",
                "source": "error",
                "confidence": 0.0
            }
            return error_response
    
    def _generate_api_response(self, user_message: str, session_id: str) -> Dict[str, Any]:
        """
        Generate a response using the Groq API
        
        Args:
            user_message (str): The user's message
            session_id (str): Session identifier for conversation tracking
            
        Returns:
            dict: Response with message and metadata
        """
        from .api_client import GroqAPIClient
        
        # Initialize API client
        client = GroqAPIClient(api_key=self.groq_api_key)
        
        # Create system message with context
        system_message = """
        You are Asha, an AI career assistant designed to help women explore career opportunities,
        job listings, professional development events, and mentorship programs. 
        You provide supportive, encouraging, and bias-free guidance.
        Keep responses concise and focused on empowering women in their careers.
        """
        
        # Retrieve relevant context from RAG pipeline
        try:
            context = self.rag_pipeline.retrieve_context(user_message)
            if context:
                system_message += f"\n\nRelevant context for this query: {context}"
        except Exception as e:
            logger.warning(f"Error retrieving context from RAG pipeline: {str(e)}")
        
        # Prepare conversation history for API
        messages = [{"role": "system", "content": system_message}]
        
        # Add relevant conversation history (last 5 exchanges)
        if len(self.conversation_history[session_id]) > 0:
            messages.extend(self.conversation_history[session_id][-min(10, len(self.conversation_history[session_id])):])
        
        # Make API call
        try:
            response = client.chat_completion(messages)
            
            if response and "choices" in response and len(response["choices"]) > 0:
                bot_message = response["choices"][0]["message"]["content"]
                return {
                    "message": bot_message,
                    "source": "groq_api",
                    "model": self.model,
                    "confidence": 0.95
                }
            else:
                raise ValueError("Invalid response format from API")
                
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise
    
    def _generate_local_response(self, user_message: str) -> Dict[str, Any]:
        """
        Generate a response using local methods when API is not available
        
        Args:
            user_message (str): The user's message
            
        Returns:
            dict: Response with message and metadata
        """
        # In a real implementation, this would use more sophisticated local methods
        # For this example, we'll use a simple set of predefined responses
        
        user_message_lower = user_message.lower()
        
        if any(keyword in user_message_lower for keyword in ["hello", "hi", "hey", "greetings"]):
            return {
                "message": "Hello! I'm Asha, your career assistant. How can I help with your professional journey today?",
                "source": "template",
                "confidence": 0.8
            }
        elif any(keyword in user_message_lower for keyword in ["job", "career", "work", "position"]):
            return {
                "message": "I'd be happy to help with your job search! To provide the most relevant opportunities, could you share more about your experience, skills, and what type of role you're looking for?",
                "source": "template",
                "confidence": 0.8
            }
        elif any(keyword in user_message_lower for keyword in ["resume", "cv", "portfolio"]):
            return {
                "message": "Creating a strong resume is crucial. Here are some key tips: 1) Tailor it to each job application, 2) Use action verbs, 3) Quantify achievements, 4) Keep formatting consistent, and 5) Have others review it. Would you like more specific advice?",
                "source": "template",
                "confidence": 0.8
            }
        elif any(keyword in user_message_lower for keyword in ["interview", "preparing"]):
            return {
                "message": "Preparing for interviews is essential! Research the company, practice common questions, prepare concrete examples of your achievements, and develop thoughtful questions to ask. Would you like interview tips for a specific industry?",
                "source": "template",
                "confidence": 0.8
            }
        else:
            # Use RAG pipeline for more complex queries
            try:
                context = self.rag_pipeline.retrieve_context(user_message)
                if context:
                    return {
                        "message": f"Based on my knowledge: {context}\n\nIs there anything specific about this you'd like to know more about?",
                        "source": "rag",
                        "confidence": 0.7
                    }
            except Exception as e:
                logger.warning(f"Error using RAG pipeline: {str(e)}")
            
            # Default response
            return {
                "message": "I'm here to help with your career questions. Could you provide more details about what you're looking for assistance with?",
                "source": "default",
                "confidence": 0.5
            }
    
    def clear_conversation(self, session_id: str = None) -> None:
        """
        Clear the conversation history
        
        Args:
            session_id (str, optional): Session to clear. If None, clears all sessions.
        """
        if session_id:
            if session_id in self.conversation_history:
                del self.conversation_history[session_id]
                logger.info(f"Conversation history cleared for session {session_id}")
        else:
            self.conversation_history = {}
            logger.info("All conversation history cleared")
        
    def get_conversation_history(self, session_id: str = None) -> List[Dict[str, str]]:
        """
        Get the conversation history
        
        Args:
            session_id (str, optional): Session to retrieve. If None, returns all sessions.
            
        Returns:
            List of conversation messages
        """
        if session_id:
            return self.conversation_history.get(session_id, [])
        return self.conversation_history 