from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path for importing from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Define absolute paths for Flask app
template_dir = os.path.join(current_dir, 'templates')
static_dir = os.path.join(current_dir, 'static')

app = Flask(__name__, 
            static_url_path='/static',
            static_folder=static_dir,
            template_folder=template_dir)

# Import and register API routes blueprint
try:
    # First try relative import (for deployment)
    from .api_routes import api
except ImportError:
    # Fall back to direct import (for local development)
    from api_routes import api

app.register_blueprint(api, url_prefix='/api')

# Custom static files handler with stricter cache control
@app.route('/static/<path:path>')
def serve_static(path):
    response = make_response(send_from_directory(static_dir, path))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.after_request
def add_cache_control(response):
    """Add cache control headers to all responses"""
    # Prevent caching for HTML responses
    if response.mimetype == 'text/html':
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

@app.route('/')
def home():
    """Render the main chat interface"""
    # Add timestamp to force template refresh but handle file not found gracefully
    template_path = os.path.join(template_dir, 'index.html')
    
    if os.path.exists(template_path):
        timestamp = int(os.path.getmtime(template_path))
    else:
        logger.error(f"Template file not found: {template_path}")
        timestamp = int(0)
        
    return render_template('index.html', cache_bust=timestamp)

@app.route('/manifest.json')
def manifest():
    """Serve the manifest file for PWA support"""
    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')
def service_worker():
    """Serve the service worker file for PWA support"""
    return app.send_static_file('service-worker.js')

if __name__ == '__main__':
    logger.info(f"Template directory: {template_dir}")
    logger.info(f"Static directory: {static_dir}")
    
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Asha Chatbot on port {port}")
    # Use debug=False for production
    app.run(host='0.0.0.0', port=port, debug=True) 