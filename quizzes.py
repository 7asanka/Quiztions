"""
Quizzes blueprint for Quiztions API
"""
from flask import Blueprint, jsonify
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import get_db
from utils.auth_helpers import token_required

# Create the quizzes blueprint
quiz_routes = Blueprint('quiz_routes', __name__)

@quiz_routes.route('/quizzes', methods=['GET'])
@token_required
def get_quizzes(user_id):
    """
    Get all quizzes (protected route)
    Returns only id, title, and description for each quiz
    """
    try:
        # Get database connection
        db = get_db()
        quizzes_collection = db.quizzes
        
        # Fetch all quizzes with limited fields
        quizzes_cursor = quizzes_collection.find(
            {},
            {
                '_id': 1,
                'title': 1,
                'description': 1
            }
        )
        
        # Convert cursor to list and format response
        quizzes = []
        for quiz in quizzes_cursor:
            quizzes.append({
                'id': str(quiz['_id']),
                'title': quiz.get('title', ''),
                'description': quiz.get('description', '')
            })
        
        return jsonify({
            'message': 'Quizzes retrieved successfully',
            'quizzes': quizzes,
            'count': len(quizzes)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@quiz_routes.route('/quizzes/<quiz_id>', methods=['GET'])
@token_required
def get_quiz_by_id(user_id, quiz_id):
    """
    Get a specific quiz by ID (protected route)
    Returns full quiz details including questions
    """
    try:
        # Validate quiz_id format
        try:
            quiz_object_id = ObjectId(quiz_id)
        except InvalidId:
            return jsonify({
                'error': 'Invalid quiz ID format'
            }), 400
        
        # Get database connection
        db = get_db()
        quizzes_collection = db.quizzes
        
        # Fetch the quiz by ID
        quiz = quizzes_collection.find_one({'_id': quiz_object_id})
        
        if not quiz:
            return jsonify({
                'error': 'Quiz not found'
            }), 404
        
        # Format the response
        quiz_data = {
            'id': str(quiz['_id']),
            'title': quiz.get('title', ''),
            'description': quiz.get('description', ''),
            'questions': quiz.get('questions', [])
        }
        
        return jsonify({
            'message': 'Quiz retrieved successfully',
            'quiz': quiz_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500