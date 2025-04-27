# src/context_manager.py
class ContextManager:
    def __init__(self, context_window=5):
        self.context_window = context_window
        self.conversations = {}
    
    def add_interaction(self, session_id, user_query, bot_response):
        """Add a new interaction to the conversation history"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            "user": user_query,
            "bot": bot_response
        })
        
        # Maintain context window size
        if len(self.conversations[session_id]) > self.context_window:
            self.conversations[session_id] = self.conversations[session_id][-self.context_window:]
    
    def get_context(self, session_id):
        """Get current conversation context"""
        if session_id in self.conversations:
            return self.conversations[session_id]
        return []
    
    def clear_context(self, session_id):
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            del self.conversations[session_id]