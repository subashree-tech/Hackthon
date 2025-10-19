#!/usr/bin/env python
"""
Simple script to run the Flask application
"""
import os
import sys
from app import app

if __name__ == '__main__':
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("WARNING: .env file not found!")
        print("Please create a .env file with your API keys.")
        print("You can copy env.example to .env and fill in your keys.")
        print("\nRunning in demo mode (limited functionality)...\n")
    
    # Check if required directories exist
    for directory in ['static/uploads', 'static/outputs']:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"[OK] Created directory: {directory}")
    
    print("\n" + "="*50)
    print("Kids Coloring Page Generator")
    print("="*50)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress CTRL+C to stop the server\n")
    
    # Run the Flask app
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV', 'development') == 'development'
    )

