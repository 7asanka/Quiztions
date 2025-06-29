"""
Database connection module for Quiztions API
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'quiztsions')

# Global database connection
client = None
db = None

def connect_to_mongo():
    """
    Establish connection to MongoDB
    """
    global client, db
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        # Test the connection
        client.admin.command('ping')
        print(f"Connected to MongoDB database: {DATABASE_NAME}")
        return db
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

def get_db():
    """
    Get the database instance
    """
    global db
    if db is None:
        db = connect_to_mongo()
    return db

def close_connection():
    """
    Close the MongoDB connection
    """
    global client
    if client:
        client.close()
        print("MongoDB connection closed")
