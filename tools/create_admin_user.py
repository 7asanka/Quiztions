#!/usr/bin/env python3
"""
Utility script to create an admin user for testing admin-only endpoints
"""
import os
from werkzeug.security import generate_password_hash
from db import connect_to_mongo, get_db
from dotenv import load_dotenv

def create_admin_user():
    """
    Create an admin user in the database
    """
    # Load environment variables
    load_dotenv()
    
    try:
        # Connect to database
        connect_to_mongo()
        db = get_db()
        users_collection = db.users
        
        # Admin user details
        admin_email = "admin@quiztions.com"
        admin_password = "admin123"  # Change this for production!
        
        # Check if admin user already exists
        existing_admin = users_collection.find_one({'email': admin_email})
        if existing_admin:
            print(f"Admin user '{admin_email}' already exists!")
            
            # Update existing user to have admin privileges
            users_collection.update_one(
                {'email': admin_email},
                {'$set': {'is_admin': True}}
            )
            print(f"Updated '{admin_email}' to have admin privileges.")
            return
        
        # Hash the password
        hashed_password = generate_password_hash(admin_password)
        
        # Create admin user document
        admin_doc = {
            'email': admin_email,
            'password': hashed_password,
            'is_admin': True
        }
        
        # Insert admin user into database
        result = users_collection.insert_one(admin_doc)
        
        print(f"Admin user created successfully!")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
        print(f"User ID: {str(result.inserted_id)}")
        print("\n⚠️  IMPORTANT: Change the default admin password for production use!")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    create_admin_user()
