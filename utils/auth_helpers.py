"""
Authentication helpers for JWT token validation
"""
import jwt
from functools import wraps
from flask import request, jsonify, current_app
from db import get_db
from bson.objectid import ObjectId
import os

def token_required(f):
    """
    Decorator to require JWT token authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check for token in x-access-token header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({
                'error': 'Token is missing'
            }), 401
        
        try:
            # Get secret key - try current_app first, fallback to env
            try:
                secret_key = current_app.config['SECRET_KEY']
            except:
                secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
            
            # Decode the token
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = data['user_id']
            
            # Verify user exists in database
            db = get_db()
            user = db.users.find_one({'_id': ObjectId(user_id)})
            
            if not user:
                return jsonify({
                    'error': 'Invalid token - user not found'
                }), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': 'Token has expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'error': 'Invalid token'
            }), 401
        except Exception as e:
            return jsonify({
                'error': f'Token validation failed: {str(e)}'
            }), 401
        
        # Pass user_id to the protected route
        return f(user_id, *args, **kwargs)
    
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin privileges
    Must be used after token_required decorator
    """
    @wraps(f)
    def decorated_function(user_id, *args, **kwargs):
        try:
            # Get database connection
            db = get_db()
            users_collection = db.users
            
            # Find user and check admin status
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            
            if not user:
                return jsonify({
                    'error': 'User not found'
                }), 403
            
            # Check if user is admin
            if not user.get('is_admin', False):
                return jsonify({
                    'error': 'Admin privileges required'
                }), 403
            
            # User is admin, proceed to the route
            return f(user_id, *args, **kwargs)
            
        except Exception as e:
            return jsonify({
                'error': f'Admin validation failed: {str(e)}'
            }), 403
    
    return decorated_function
