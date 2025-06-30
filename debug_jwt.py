"""
Debug script to test JWT token generation and validation
"""
import jwt
from datetime import datetime, timedelta

# Test the token generation and validation manually
SECRET_KEY = 'your-secret-key-change-this-in-production'
user_id = "6862a9bc30d48268d67dd97d"
email = "newuser@example.com"

# Generate a token
token_payload = {
    'user_id': user_id,
    'email': email,
    'exp': datetime.utcnow() + timedelta(hours=24)
}

token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
print(f"Generated token: {token}")

# Try to decode it
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    print(f"Decoded successfully: {decoded}")
except Exception as e:
    print(f"Decode error: {e}")
