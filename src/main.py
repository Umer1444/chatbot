import sys
import asyncio
import os

# 🛠 Fix for torch + Streamlit on Windows (event loop issue)
if sys.platform.startswith('win'):
    try:
        # Check if the current thread already has an event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no event loop exists, create one and set it for the current thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# 🧹 Optional: Clean up logs from transformers
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

# Standard imports
import uuid
from src.rag_pipeline import RAGPipeline  # Correct path to rag_pipeline
from src.context_manager import ContextManager  # Correct path to context_manager
from src.bias_detection import BiasDetectionModule  # Correct path to bias_detection

class AshaAIBot:
    def __init__(self):
        # Initialize the pipeline, context manager, and bias detection module
        self.rag_pipeline = RAGPipeline()
        self.context_manager = ContextManager()  # Instantiate the ContextManager
        self.bias_detector = BiasDetectionModule()
        
    def process_query(self, query, session_id=None):
        """Process user query and generate response."""
        if not session_id:
            session_id = str(uuid.uuid4())  # Generate a new session ID if none is provided
            
        # Check for bias
        is_biased, biased_term = self.bias_detector.detect_bias(query)
        if is_biased:
            alternative = self.bias_detector.suggest_alternative(biased_term)
            response = {
                "type": "bias_detected",
                "message": f"I'd like to provide helpful information. {alternative}",
                "session_id": session_id
            }
            self.context_manager.add_interaction(session_id, query, response)  # Log the biased query and response
            return response
        
        # Get conversation context from the ContextManager
        context = self.context_manager.get_context(session_id)
        
        # Retrieve information using the RAG pipeline
        retrieved_info = self.rag_pipeline.retrieve_information(query)
        
        # Generate response based on the retrieved information
        response = self.generate_response(query, retrieved_info, context)
        
        # Update the context with the new query and response
        self.context_manager.add_interaction(session_id, query, response)
        
        return {
            "type": "normal",
            "message": response,
            "retrieved_data": retrieved_info.get("data", []),  # Attach the retrieved data
            "session_id": session_id
        }
    
    def generate_response(self, query, retrieved_info, context):
        """Generate a natural language response based on the retrieved information."""
        source = retrieved_info.get("source")
        data = retrieved_info.get("data", [])
        
        if source == "jobs" and data:
            # Format job information if the source is 'jobs'
            job_responses = []
            for job in data:
                job_info = f"I found a {job['job_title']} position at {job['company']} in {job['location']}. "
                job_info += f"It's in the {job['industry']} industry and was posted on {job['posted_date']}. "
                job_info += f"You can apply at: {job['apply_link']}"
                job_responses.append(job_info)
                
            response = "Here are some job opportunities that might interest you:\n\n" + "\n\n".join(job_responses)
            return response
        
        # Default response for other queries
        return "I'm Asha, your career assistant. I can help you find job opportunities, mentorship programs, and professional development resources. What specific information are you looking for today?"
