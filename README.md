# Quiztions API

A comprehensive Flask-based REST API for creating and managing interactive quizzes with JWT authentication and role-based access control.

## 🚀 Features

- **User Authentication** - JWT-based registration and login
- **Quiz Management** - Create, view, and take quizzes
- **Role-Based Access** - Admin-only quiz creation
- **Results Tracking** - Automatic scoring and history
- **MongoDB Integration** - Scalable data storage
- **Production Ready** - Waitress WSGI server for deployment

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Database Schema](#database-schema)
- [Development Tools](#development-tools)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/7asanka/Quiztions.git
   cd Quiztions
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**
   - Install and start MongoDB on your system
   - The API will create the `quiztions` database automatically

## ⚙️ Configuration

1. **Environment Variables**
   Copy `.env.example` to `.env` and configure:
   ```env
   SECRET_KEY=your-super-secret-jwt-key-here
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_DATABASE=quiztions
   ```

2. **Create Admin User** (Optional)
   ```bash
   python tools/create_admin_user.py
   ```

## 🚀 Running the Server

### Development Server
```bash
python app.py
```

### Production Server (Recommended)
```bash
python run_production.py
```

The API will be available at `http://localhost:5000`

## 📚 API Endpoints

### 📝 Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "User already exists"
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": "507f1f77bcf86cd799439011"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

### 🧩 Quiz Endpoints

#### Get All Quizzes
```http
GET /api/quizzes
x-access-token: YOUR_JWT_TOKEN
```

**Response (200 OK):**
```json
{
  "count": 2,
  "quizzes": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "Python Basics",
      "description": "Test your Python knowledge"
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "title": "JavaScript Fundamentals",
      "description": "JavaScript quiz for beginners"
    }
  ]
}
```

#### Get Quiz Details
```http
GET /api/quizzes/507f1f77bcf86cd799439011
x-access-token: YOUR_JWT_TOKEN
```

**Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Python Basics",
  "description": "Test your Python knowledge",
  "questions": [
    {
      "text": "What is Python?",
      "options": [
        "A programming language",
        "A snake",
        "A framework",
        "A database"
      ],
      "correct_answer": 0
    }
  ]
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Quiz not found"
}
```

#### Submit Quiz Answers
```http
POST /api/quizzes/507f1f77bcf86cd799439011/submit
Content-Type: application/json
x-access-token: YOUR_JWT_TOKEN

{
  "answers": [0, 2, 1]
}
```

**Response (200 OK):**
```json
{
  "message": "Quiz submitted successfully",
  "score": 66.67,
  "correct_answers": 2,
  "total_questions": 3,
  "submitted_at": "2024-01-15T10:30:45.123000"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Number of answers (2) does not match number of questions (3)"
}
```

#### Create Quiz (Admin Only)
```http
POST /api/quizzes/create
Content-Type: application/json
x-access-token: YOUR_ADMIN_JWT_TOKEN

{
  "title": "Advanced Python",
  "description": "Advanced Python concepts",
  "questions": [
    {
      "text": "What is a decorator?",
      "options": [
        "A function that modifies another function",
        "A design pattern",
        "A data structure",
        "A module"
      ],
      "correct_answer": 0
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "message": "Quiz created successfully",
  "quiz_id": "507f1f77bcf86cd799439013",
  "title": "Advanced Python"
}
```

**Error Response (403 Forbidden):**
```json
{
  "error": "Admin privileges required"
}
```

### 📊 Results Endpoints

#### Get User Results
```http
GET /api/results
x-access-token: YOUR_JWT_TOKEN
```

**Response (200 OK):**
```json
{
  "count": 2,
  "results": [
    {
      "quiz_id": "507f1f77bcf86cd799439011",
      "score": 85.0,
      "correct_answers": 17,
      "total_questions": 20,
      "submitted_at": "2024-01-15T10:30:45.123000"
    },
    {
      "quiz_id": "507f1f77bcf86cd799439012",
      "score": 70.0,
      "correct_answers": 7,
      "total_questions": 10,
      "submitted_at": "2024-01-14T15:22:30.456000"
    }
  ]
}
```

## 🔐 Authentication

### JWT Token Usage

1. **Obtain Token**: Call `/auth/login` with valid credentials
2. **Use Token**: Include in `x-access-token` header for protected routes
3. **Token Expiry**: Tokens expire after 24 hours

### Protected Routes

All routes except `/auth/register` and `/auth/login` require a valid JWT token:

```http
x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Admin Routes

Routes marked as admin-only require the user to have `is_admin: true` in their database record:

- `POST /api/quizzes/create`

## ❌ Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid token |
| 403 | Forbidden - Insufficient privileges |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "error": "Descriptive error message"
}
```

## 🗄️ Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "password": "hashed_password",
  "is_admin": false,
  "created_at": ISODate("...")
}
```

### Quizzes Collection
```javascript
{
  "_id": ObjectId("..."),
  "title": "Quiz Title",
  "description": "Quiz description",
  "questions": [
    {
      "text": "Question text?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correct_answer": 0
    }
  ],
  "created_at": ISODate("...")
}
```

### Results Collection
```javascript
{
  "_id": ObjectId("..."),
  "user_id": ObjectId("..."),
  "quiz_id": ObjectId("..."),
  "score": 85.5,
  "correct_answers": 17,
  "total_questions": 20,
  "submitted_at": ISODate("...")
}
```

## 🛠️ Development Tools

### Available Scripts

- `tools/create_admin_user.py` - Create admin users
- `tools/test_api.py` - Comprehensive API testing

### Testing

1. **Create Admin User**:
   ```bash
   python tools/create_admin_user.py
   ```

2. **Run API Tests**:
   ```bash
   python tools/test_api.py
   ```

### Project Structure

```
Quiztions/
├── app.py                  # Main Flask application
├── auth.py                 # Authentication routes
├── quizzes.py             # Quiz management routes
├── results.py             # Results tracking routes
├── db.py                  # Database connection
├── run_production.py      # Production server
├── requirements.txt       # Dependencies
├── utils/
│   └── auth_helpers.py    # JWT authentication decorators
└── tools/
    ├── create_admin_user.py
    ├── test_api.py
    └── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

**Happy Quizzing!** 🎯