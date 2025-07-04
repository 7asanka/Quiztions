# Development Tools

This directory contains development and testing utilities for the Quiztions API.

## Files

### `create_admin_user.py`
Creates an admin user in the MongoDB database for testing admin-only endpoints.

**Usage:**
```bash
python tools/create_admin_user.py
```

**Default Admin Credentials:**
- Email: `admin@quiztions.com`
- Password: `admin123`

⚠️ **Important:** Change the default password for production use!

### `test_api.py`
Comprehensive API testing script that tests all endpoints including:
- User registration and authentication
- Admin authentication and quiz creation
- Quiz listing, details, submission
- Results retrieval
- Error handling scenarios

**Usage:**
```bash
# Make sure the API server is running first
python app.py
# or
python run_production.py

# Then run the tests
python tools/test_api.py
```

## Requirements

These tools require the `requests` library which should be installed automatically with:
```bash
pip install -r requirements.txt
```

## Notes

- Make sure MongoDB is running before using these tools
- The API server must be running on `http://localhost:5000` for the test script
- These tools are for development and testing purposes only
