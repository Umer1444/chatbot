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

app = Flask(__name__, 
            static_url_path='/static',
            static_folder='static',
            template_folder='templates')

# Import and register API routes blueprint
from api_routes import api
app.register_blueprint(api, url_prefix='/api')

# Custom static files handler to prevent caching
@app.route('/static/<path:path>')
def serve_static(path):
    response = make_response(send_from_directory('static', path))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    """Serve the manifest file for PWA support"""
    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')
def service_worker():
    """Serve the service worker file for PWA support"""
    return app.send_static_file('service-worker.js')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Asha Chatbot on port {port}")
    # Use debug=False for production
    app.run(host='0.0.0.0', port=port, debug=True) 