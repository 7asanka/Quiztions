# Admin Quiz Creation Testing Guide

This guide explains how to test the admin-only quiz creation functionality in Quiztions.

## Prerequisites

1. Make sure you have Python 3.7+ installed
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure MongoDB is running
4. Create a `.env` file with your MongoDB connection string and secret key

## Step 1: Create Admin User

First, create an admin user in the database:

```bash
python tools/create_admin_user.py
```

This will create an admin user with:
- Email: `admin@quiztions.com`
- Password: `admin123`
- Admin privileges: `True`

## Step 2: Start the API Server

Start the Flask development server:

```bash
python app.py
```

The server will run on `http://localhost:5000`

## Step 3: Test Admin Functionality

### Option A: Use the Test Script (Recommended)

Run the comprehensive test script:

```bash
python tools/test_api.py
```

This will automatically test all endpoints including:
- User registration and login
- Admin login
- Regular user attempting quiz creation (should fail)
- Admin user creating quiz (should succeed)
- Getting quizzes, quiz details, submitting quizzes, and viewing results

### Option B: Manual Testing with curl or Postman

#### 1. Login as Admin
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@quiztions.com", "password": "admin123"}'
```

Copy the token from the response.

#### 2. Create a Quiz (Admin Only)
```bash
curl -X POST http://localhost:5000/api/quizzes/create \
  -H "Content-Type: application/json" \
  -H "x-access-token: YOUR_ADMIN_TOKEN_HERE" \
  -d '{
    "title": "Sample Quiz",
    "description": "A test quiz for demonstration",
    "questions": [
      {
        "text": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": 1
      },
      {
        "text": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "correct_answer": 1
      }
    ]
  }'
```

#### 3. Test with Regular User (Should Fail)
First, register and login as a regular user, then try to create a quiz with their token. It should return a 403 Forbidden error.

## API Endpoints Summary

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | GET | Public | API information |
| `/auth/register` | POST | Public | Register new user |
| `/auth/login` | POST | Public | Login user |
| `/api/quizzes` | GET | User Token | Get all quizzes |
| `/api/quizzes/<id>` | GET | User Token | Get specific quiz |
| `/api/quizzes/<id>/submit` | POST | User Token | Submit quiz answers |
| `/api/results` | GET | User Token | Get user's results |
| `/api/quizzes/create` | POST | **Admin Token** | Create new quiz |

## Quiz Creation Request Format

```json
{
  "title": "Quiz Title",
  "description": "Quiz description",
  "questions": [
    {
      "text": "Question text?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correct_answer": 1
    }
  ]
}
```

## Security Features

- JWT token authentication for all protected routes
- Admin role verification for quiz creation
- Input validation for all quiz data
- Proper error handling and status codes

## Notes

- The `correct_answer` field should be an integer index (0-based) of the correct option
- All questions must have at least 2 options
- Admin privileges are checked via the `is_admin` field in the user document
- Tokens are passed in the `x-access-token` header
