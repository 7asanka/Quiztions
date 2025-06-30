"""
Quiztions Flask API Application
"""
import os
from flask import Flask, jsonify
from auth import auth_blueprint
from results import results_blueprint
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

@app.route('/')
def index():
    """
    API root endpoint
    """
    return jsonify({
        'message': 'Welcome to Quiztions API!',
        'version': '1.0',
        'endpoints': {
            'register': '/auth/register (POST)',
            'login': '/auth/login (POST)',
            'results': '/api/results (GET - requires token)'
        }
    })

if __name__ == '__main__':
    # For Windows compatibility, disable reloader
    # For production use, run with: python run_production.py
    print("Starting development server...")
    print("For production use, run: python run_production.py")
    app.run(debug=True, port=5000, host='localhost', use_reloader=False, threaded=True)