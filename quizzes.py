"""
Quizzes blueprint for Quiztions API
"""
from flask import Blueprint, jsonify, request
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

@quiz_routes.route('/quizzes/<quiz_id>/submit', methods=['POST'])
@token_required
def submit_quiz(user_id, quiz_id):
    """
    Submit quiz answers and calculate score (protected route)
    """
    try:
        # Validate quiz_id format
        try:
            quiz_object_id = ObjectId(quiz_id)
        except InvalidId:
            return jsonify({
                'error': 'Invalid quiz ID format'
            }), 400
        
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400
        
        # Validate answers array
        answers = data.get('answers')
        if answers is None:
            return jsonify({
                'error': 'Answers array is required'
            }), 400
        
        if not isinstance(answers, list):
            return jsonify({
                'error': 'Answers must be an array'
            }), 400
        
        # Get database connection
        db = get_db()
        quizzes_collection = db.quizzes
        
        # Fetch the quiz
        quiz = quizzes_collection.find_one({'_id': quiz_object_id})
        if not quiz:
            return jsonify({
                'error': 'Quiz not found'
            }), 404
        
        questions = quiz.get('questions', [])
        
        # Validate answers count
        if len(answers) != len(questions):
            return jsonify({
                'error': f'Expected {len(questions)} answers, got {len(answers)}'
            }), 400
        
        # Calculate score
        correct_answers = 0
        total_questions = len(questions)
        
        for i, (user_answer, question) in enumerate(zip(answers, questions)):
            correct_answer = question.get('correct_answer')
            
            # Validate answer format (should be integer index)
            if not isinstance(user_answer, int):
                return jsonify({
                    'error': f'Answer at index {i} must be an integer (option index)'
                }), 400
            
            # Check if answer is within valid range
            if user_answer < 0 or user_answer >= len(question.get('options', [])):
                return jsonify({
                    'error': f'Answer at index {i} is out of range'
                }), 400
            
            # Check if answer is correct
            if user_answer == correct_answer:
                correct_answers += 1
        
        # Calculate score as percentage
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Store result in database
        from datetime import datetime
        results_collection = db.results
        
        result_doc = {
            'user_id': user_id,
            'quiz_id': str(quiz_object_id),
            'score': round(score, 2),
            'submitted_at': datetime.utcnow(),
            'correct_answers': correct_answers,
            'total_questions': total_questions
        }
        
        result = results_collection.insert_one(result_doc)
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'result_id': str(result.inserted_id),
            'score': round(score, 2),
            'correct_answers': correct_answers,
            'total_questions': total_questions
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500