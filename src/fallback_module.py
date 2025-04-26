# src/fallback_module.py
class FallbackModule:
    def __init__(self):
        self.generic_responses = [
            "I'm not sure I have enough information to answer that question. Could you provide more details?",
            "I don't have specific information about that. Would you like me to help with job listings or mentorship programs instead?",
            "That's outside my current knowledge. I can help you with career opportunities, professional development, and mentorship programs.",
            "I'm still learning about that area. Can I help you with something related to job searching or career development?"
        ]
        
    def get_fallback_response(self, query=None, context=None):
        """Provide a relevant fallback response when the system cannot answer confidently"""
        # Simple implementation - in production, this would be more sophisticated
        import random
        return random.choice(self.generic_responses)
    
    def should_fallback(self, confidence_score):
        """Determine if the system should use a fallback response"""
        # Simple threshold-based decision
        return confidence_score < 0.4