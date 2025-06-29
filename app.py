"""
Quiztions Flask API Application
"""
from flask import Flask, jsonify
from auth import auth_blueprint
from db import connect_to_mongo, close_connection
import atexit

app = Flask(__name__)

# Initialize database connection
try:
    connect_to_mongo()
except Exception as e:
    print(f"Failed to connect to database: {e}")

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')

@app.route('/')
def index():
    """
    API root endpoint
    """
    return jsonify({
        'message': 'Welcome to Quiztions API!',
        'version': '1.0',
        'endpoints': {
            'register': '/auth/register (POST)'
        }
    })

# Clean up database connection on app shutdown
atexit.register(close_connection)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='localhost')