#!/usr/bin/env python3
"""
Database setup script for Social Support AI System
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Parse connection string to get database name
        db_url = settings.database_url
        if db_url.startswith('postgresql://'):
            # Extract database name from URL
            parts = db_url.split('/')
            if len(parts) >= 4:
                db_name = parts[-1]
                # Create connection string without database name
                base_url = '/'.join(parts[:-1])
                
                # Connect to PostgreSQL server
                conn = psycopg2.connect(base_url)
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = conn.cursor()
                
                # Check if database exists
                cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
                exists = cursor.fetchone()
                
                if not exists:
                    print(f"Creating database: {db_name}")
                    cursor.execute(f'CREATE DATABASE "{db_name}"')
                    print(f"Database '{db_name}' created successfully")
                else:
                    print(f"Database '{db_name}' already exists")
                
                cursor.close()
                conn.close()
            else:
                print("Invalid database URL format")
                return False
        else:
            print("Database URL must start with 'postgresql://'")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def create_tables():
    """Create database tables"""
    try:
        from app.core.database import init_db
        print("Creating database tables...")
        init_db()
        print("Database tables created successfully")
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def insert_sample_data():
    """Insert sample data for testing"""
    try:
        from app.core.database import get_db
        from app.models.database_models import Applicant, Document
        
        print("Inserting sample data...")
        
        # This would insert sample data for testing
        # For now, just print a message
        print("Sample data insertion skipped (implement as needed)")
        return True
        
    except Exception as e:
        print(f"Error inserting sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up Social Support AI System Database...")
    print("=" * 50)
    
    # Create database
    if not create_database():
        print("Failed to create database")
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        print("Failed to create tables")
        sys.exit(1)
    
    # Insert sample data
    if not insert_sample_data():
        print("Failed to insert sample data")
        sys.exit(1)
    
    print("=" * 50)
    print("Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the FastAPI backend: uvicorn app.main:app --reload")
    print("2. Start the Streamlit UI: streamlit run app/streamlit_app.py")
    print("3. Ensure Ollama is running for LLM functionality")

if __name__ == "__main__":
    main() 