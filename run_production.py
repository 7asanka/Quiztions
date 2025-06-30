"""
Production-ready server using Waitress WSGI server
This avoids all the Windows socket issues with Flask's dev server
"""
from waitress import serve
from app import app

if __name__ == '__main__':
    print("Starting Quiztions API server with Waitress...")
    print("Server will be available at: http://localhost:5000")
    print("This server is production-ready and stable on Windows")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Use Waitress instead of Flask's development server
        serve(
            app, 
            host='localhost', 
            port=5000,
            threads=6,  # Handle multiple requests
            cleanup_interval=30,
            channel_timeout=120
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")
