"""
Alternative way to run the Flask application
This script helps avoid the Windows socket error
"""
from app import app

if __name__ == '__main__':
    print("Starting Quiztions API server...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Run with minimal configuration to avoid threading issues
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")
