"""
Results blueprint for Quiztions API
"""
from flask import Blueprint, jsonify
from db import get_db
from utils.auth_helpers import token_required

# Create the results blueprint
results_blueprint = Blueprint('results', __name__)

@results_blueprint.route('/results', methods=['GET'])
@token_required
def get_results(user_id):
    """
    Get all quiz results for authenticated user
    Protected route that requires JWT token
    """
    try:
        # Get database connection
        db = get_db()
        results_collection = db.results
        
        # Fetch all results for the user
        user_results = results_collection.find({'user_id': user_id}).sort('submitted_at', -1)
        
        # Format results
        results = []
        for result in user_results:
            results.append({
                'result_id': str(result['_id']),
                'quiz_id': result.get('quiz_id'),
                'score': result.get('score'),
                'submitted_at': result.get('submitted_at').isoformat() if result.get('submitted_at') else None,
                'correct_answers': result.get('correct_answers'),
                'total_questions': result.get('total_questions')
            })
        
        return jsonify({
            'message': 'Results retrieved successfully',
            'user_id': user_id,
            'results': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500