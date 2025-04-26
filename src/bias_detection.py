# src/bias_detection.py
import re

class BiasDetectionModule:
    def __init__(self):
        # Words/phrases that might indicate gender bias
        self.potentially_biased_terms = [
            "women can't", "women should", "all women are", 
            "females are not good at", "women belong", 
            "men are better"
        ]
        
    def detect_bias(self, text):
        """Check for potentially biased language in user queries"""
        text_lower = text.lower()
        
        for term in self.potentially_biased_terms:
            if term in text_lower:
                return True, term
                
        return False, None
    
    def suggest_alternative(self, biased_term):
        """Provide suggestions for rephrasing biased queries"""
        alternatives = {
            "women can't": "What are successful approaches in this field?",
            "women should": "What are the best practices in this profession?",
            # Add more alternatives
        }
        
        for term, suggestion in alternatives.items():
            if term in biased_term:
                return suggestion
                
        return "Could you rephrase your question to focus on skills and qualifications?"