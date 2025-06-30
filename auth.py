"""
Authentication blueprint for Quiztions API
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from db import get_db
import jwt
from datetime import datetime, timedelta

# Create the auth blueprint
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Check for missing fields
        if not email:
            return jsonify({
                'error': 'Email is required'
            }), 400
        
        if not password:
            return jsonify({
                'error': 'Password is required'
            }), 400
        
        # Get database connection
        db = get_db()
        users_collection = db.users
        
        # Check if user already exists
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return jsonify({
                'error': 'User with this email already exists'
            }), 409
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Create user document
        user_doc = {
            'email': email,
            'password': hashed_password
        }
        
        # Insert user into database
        result = users_collection.insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        # Return success response
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Check for missing fields
        if not email:
            return jsonify({
                'error': 'Email is required'
            }), 400
        
        if not password:
            return jsonify({
                'error': 'Password is required'
            }), 400
        
        # Get database connection
        db = get_db()
        users_collection = db.users
        
        # Find user by email
        user = users_collection.find_one({'email': email})
        if not user:
            return jsonify({
                'error': 'Invalid credentials'
            }), 401
        
        # Check password
        if not check_password_hash(user['password'], password):
            return jsonify({
                'error': 'Invalid credentials'
            }), 401
        
        # Generate JWT token
        token_payload = {
            'user_id': str(user['_id']),
            'email': user['email'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(
            token_payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        # Return success response with token
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user_id': str(user['_id'])
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500