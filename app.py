"""
Quiztions Flask API Application
"""
import os
from flask import Flask, jsonify, send_from_directory
from auth import auth_blueprint
from results import results_blueprint
from quizzes import quiz_routes
from db import connect_to_mongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Initialize database connection
try:
    connect_to_mongo()
except Exception as e:
    print(f"Failed to connect to database: {e}")

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(results_blueprint, url_prefix='/api')
app.register_blueprint(quiz_routes, url_prefix='/api')

@app.route('/')
def index():
    """
    Serve the login page as the default
    NOTE: This is for demo purposes only
    """
    return send_from_directory('.', 'login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """
    Serve static HTML files
    NOTE: This is for demo/testing purposes only
    In production, use a proper web server (nginx, Apache) or CDN
    """
    return send_from_directory('.', filename)

@app.route('/api/info')
def api_info():
    """
    API information endpoint
    """
    return jsonify({
        'message': 'Welcome to Quiztions API!',
        'version': '1.0',
        'endpoints': {
            'register': '/auth/register (POST)',
            'login': '/auth/login (POST)',
            'results': '/api/results (GET - requires token)',
            'quizzes': '/api/quizzes (GET - requires token)',
            'quiz_detail': '/api/quizzes/<quiz_id> (GET - requires token)',
            'submit_quiz': '/api/quizzes/<quiz_id>/submit (POST - requires token)',
            'create_quiz': '/api/quizzes/create (POST - requires admin token)'
        }
    })

if __name__ == '__main__':
    # For Windows compatibility, disable reloader
    # For production use, run with: python run_production.py
    print("Starting development server...")
    print("For production/stable server, run: python run_production.py")
    app.run(debug=True, port=5000, host='localhost', use_reloader=False, threaded=True)