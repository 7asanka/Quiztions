#!/usr/bin/env python3
"""
Comprehensive API testing script for Quiztions
Tests all endpoints including admin-only quiz creation
"""
import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_api():
    """
    Test all API endpoints
    """
    print("🧪 Starting Quiztions API Tests...")
    print("=" * 50)
    
    # Test variables
    admin_token = None
    regular_token = None
    quiz_id = None
    
    # 1. Test root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Register regular user
    print("\n2. Testing user registration...")
    try:
        regular_user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=regular_user_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. Login regular user
    print("\n3. Testing regular user login...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=regular_user_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        if response.status_code == 200:
            regular_token = result.get('token')
            print(f"✅ Regular user token obtained: {regular_token[:20]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # 4. Login admin user
    print("\n4. Testing admin user login...")
    try:
        admin_user_data = {
            "email": "admin@quiztions.com",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=admin_user_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        if response.status_code == 200:
            admin_token = result.get('token')
            print(f"✅ Admin token obtained: {admin_token[:20]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # 5. Test admin-only quiz creation (should fail without admin token)
    print("\n5. Testing quiz creation without admin token...")
    if regular_token:
        try:
            quiz_data = {
                "title": "Sample Quiz",
                "description": "A test quiz",
                "questions": [
                    {
                        "text": "What is 2 + 2?",
                        "options": ["3", "4", "5", "6"],
                        "correct_answer": 1
                    }
                ]
            }
            headers = {'x-access-token': regular_token}
            response = requests.post(f"{BASE_URL}/api/quizzes/create", json=quiz_data, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ Correctly rejected non-admin user")
        except Exception as e:
            print(f"Error: {e}")
    
    # 6. Test admin-only quiz creation (should succeed with admin token)
    print("\n6. Testing quiz creation with admin token...")
    if admin_token:
        try:
            quiz_data = {
                "title": "Mathematics Quiz",
                "description": "Basic arithmetic questions",
                "questions": [
                    {
                        "text": "What is 2 + 2?",
                        "options": ["3", "4", "5", "6"],
                        "correct_answer": 1
                    },
                    {
                        "text": "What is 5 * 3?",
                        "options": ["13", "15", "17", "20"],
                        "correct_answer": 1
                    },
                    {
                        "text": "What is 10 / 2?",
                        "options": ["4", "5", "6", "7"],
                        "correct_answer": 1
                    }
                ]
            }
            headers = {'x-access-token': admin_token}
            response = requests.post(f"{BASE_URL}/api/quizzes/create", json=quiz_data, headers=headers)
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            if response.status_code == 201:
                quiz_id = result.get('quiz_id')
                print(f"✅ Quiz created with ID: {quiz_id}")
        except Exception as e:
            print(f"Error: {e}")
    
    # 7. Test getting all quizzes
    print("\n7. Testing get all quizzes...")
    if regular_token:
        try:
            headers = {'x-access-token': regular_token}
            response = requests.get(f"{BASE_URL}/api/quizzes", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
    
    # 8. Test getting specific quiz
    print("\n8. Testing get specific quiz...")
    if regular_token and quiz_id:
        try:
            headers = {'x-access-token': regular_token}
            response = requests.get(f"{BASE_URL}/api/quizzes/{quiz_id}", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
    
    # 9. Test quiz submission
    print("\n9. Testing quiz submission...")
    if regular_token and quiz_id:
        try:
            submission_data = {
                "answers": [1, 1, 1]  # All correct answers
            }
            headers = {'x-access-token': regular_token}
            response = requests.post(f"{BASE_URL}/api/quizzes/{quiz_id}/submit", json=submission_data, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
    
    # 10. Test getting results
    print("\n10. Testing get results...")
    if regular_token:
        try:
            headers = {'x-access-token': regular_token}
            response = requests.get(f"{BASE_URL}/api/results", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 API Tests Completed!")

if __name__ == "__main__":
    print("⚠️  Make sure the Quiztions API server is running on http://localhost:5000")
    print("⚠️  Make sure you've created an admin user with: python create_admin_user.py")
    input("Press Enter to continue with testing...")
    test_api()
