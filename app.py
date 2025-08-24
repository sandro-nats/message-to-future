from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from scheduler import start_scheduler

start_scheduler()


app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Import models at the bottom to avoid circular imports
from models import FutureMessage

# Import scheduler at the bottom
from scheduler import start_scheduler

if __name__ == "__main__":
    start_scheduler()  # Start scheduler
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
