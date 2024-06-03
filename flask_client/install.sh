#!/bin/sh

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# For Unix-based systems (Linux/macOS)
. venv/bin/activate

# For Windows, you would use:
# .\venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt

# Set environment variables (you might want to source a .env file here instead)
export FLASK_APP=app.py
export FLASK_ENV=.env

# Run the Flask application
flask run
