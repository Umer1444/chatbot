"""
WSGI entry point for the Asha AI Chatbot.
This file makes it easier for Gunicorn to find and load the application.
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from app.app import app

# This is what Gunicorn will look for
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 