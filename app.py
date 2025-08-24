from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from scheduler import start_scheduler
import os

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import FutureMessage

# Serve frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# API route to send message
@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'email' not in data or 'subject' not in data or 'message' not in data or 'delivery_date' not in data:
        return jsonify({"error": "Missing data"}), 400

    new_message = FutureMessage(
        email=data['email'],
        subject=data['subject'],
        message=data['message'],
        delivery_date=data['delivery_date']
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"success": True})

if __name__ == "__main__":
    os.makedirs('instance', exist_ok=True)
    db.create_all()
    start_scheduler()
