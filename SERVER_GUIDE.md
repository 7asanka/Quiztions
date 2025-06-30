# Running the Quiztions API Server

Due to Windows compatibility issues with Flask's development server, we provide multiple ways to run the server:

## Option 1: Simple Development Server (Recommended for Development)
```bash
python run_server.py
```
This runs the server without debug mode to avoid Windows socket errors.

## Option 2: Production-Ready Server (Recommended for Testing/Production)
```bash
python run_production.py
```
This uses Waitress WSGI server which is stable and production-ready on Windows.

## Option 3: Direct Flask (May have socket errors on Windows)
```bash
python app.py
```
This may encounter socket errors due to Flask's reloader on Windows.

## API Endpoints

- **GET** `/` - API information
- **POST** `/auth/register` - User registration
- **POST** `/auth/login` - User login (returns JWT token)
- **GET** `/api/results` - Protected route (requires JWT token in x-access-token header)

## Testing Examples

### Register a user:
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Login:
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Access protected route:
```bash
curl -X GET http://localhost:5000/api/results \
  -H "x-access-token: YOUR_JWT_TOKEN_HERE"
```
