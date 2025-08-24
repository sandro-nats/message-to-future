from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Import routes at the bottom to avoid circular imports
# If you have separate route files, you can import them here
# Example: from routes import *

if __name__ == "__main__":
    from scheduler import start_scheduler
    start_scheduler()  # Start scheduler
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
