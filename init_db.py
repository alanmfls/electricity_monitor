#!/usr/bin/env python3
"""
Database initialization script
This script creates the database with the new schema including apartment_number
"""

from app import app, db

def init_database():
    """Initialize the database with all tables"""
    with app.app_context():
        # Drop all tables if they exist
        db.drop_all()
        
        # Create all tables with new schema
        db.create_all()
        
        print("Database initialized successfully!")
        print("Tables created:")
        print("- User (with apartment_number column)")
        print("- PowerReading")
        print("\nYou can now run the application with: python app.py")

if __name__ == "__main__":
    init_database()
