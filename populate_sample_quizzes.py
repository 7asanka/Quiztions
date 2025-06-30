"""
Script to populate sample quiz data for testing
"""
from db import get_db, connect_to_mongo

def create_sample_quizzes():
    """
    Create sample quizzes in the database
    """
    try:
        # Connect to database
        connect_to_mongo()
        db = get_db()
        quizzes_collection = db.quizzes
        
        # Sample quiz data
        sample_quizzes = [
            {
                "title": "Python Basics",
                "description": "Test your knowledge of Python fundamentals",
                "questions": [
                    {
                        "question": "What is the output of print('Hello World')?",
                        "options": [
                            "Hello World",
                            "hello world",
                            "Error",
                            "None"
                        ],
                        "correct_answer": 0
                    },
                    {
                        "question": "Which of the following is a Python data type?",
                        "options": [
                            "list",
                            "dict",
                            "tuple",
                            "All of the above"
                        ],
                        "correct_answer": 3
                    },
                    {
                        "question": "How do you create a function in Python?",
                        "options": [
                            "function myFunc():",
                            "def myFunc():",
                            "create myFunc():",
                            "func myFunc():"
                        ],
                        "correct_answer": 1
                    }
                ]
            },
            {
                "title": "JavaScript Fundamentals",
                "description": "Test your understanding of JavaScript basics",
                "questions": [
                    {
                        "question": "What does 'var' do in JavaScript?",
                        "options": [
                            "Declares a variable",
                            "Creates a function",
                            "Defines a class",
                            "Imports a module"
                        ],
                        "correct_answer": 0
                    },
                    {
                        "question": "Which method adds an element to the end of an array?",
                        "options": [
                            "append()",
                            "push()",
                            "add()",
                            "insert()"
                        ],
                        "correct_answer": 1
                    }
                ]
            },
            {
                "title": "Web Development Basics",
                "description": "General web development knowledge",
                "questions": [
                    {
                        "question": "What does HTML stand for?",
                        "options": [
                            "Hypertext Markup Language",
                            "High Tech Modern Language",
                            "Home Tool Markup Language",
                            "Hyperlink and Text Markup Language"
                        ],
                        "correct_answer": 0
                    },
                    {
                        "question": "Which of these is used for styling web pages?",
                        "options": [
                            "HTML",
                            "JavaScript",
                            "CSS",
                            "Python"
                        ],
                        "correct_answer": 2
                    }
                ]
            }
        ]
        
        # Clear existing quizzes (optional)
        quizzes_collection.delete_many({})
        
        # Insert sample quizzes
        result = quizzes_collection.insert_many(sample_quizzes)
        
        print(f"Successfully created {len(result.inserted_ids)} sample quizzes!")
        print("Quiz IDs:")
        for i, quiz_id in enumerate(result.inserted_ids):
            print(f"  {i+1}. {sample_quizzes[i]['title']}: {quiz_id}")
        
        return True
        
    except Exception as e:
        print(f"Error creating sample quizzes: {e}")
        return False

if __name__ == '__main__':
    create_sample_quizzes()
