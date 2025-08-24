from datetime import datetime
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, FutureMessage
from scheduler import start_scheduler

# --- Flask setup ---
app = Flask(__name__, static_folder="static")
CORS(app)

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# --- Serve frontend ---
@app.get("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

# Serve static files like CSS/JS automatically
@app.get("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# --- API routes ---
@app.post("/api/send-message")
def send_message():
    try:
        payload = request.form if request.form else (request.get_json(silent=True) or {})
        email = (payload.get("email") or "").strip()
        subject = (payload.get("subject") or "").strip()
        message = (payload.get("message") or "").strip()
        delivery_date_str = (payload.get("delivery_date") or "").strip()

        if not (email and subject and message and delivery_date_str):
            return jsonify({"error": "All fields are required."}), 400

        try:
            delivery_date = datetime.strptime(delivery_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "delivery_date must be in YYYY-MM-DD format."}), 400

        new_msg = FutureMessage(
            email=email,
            subject=subject,
            message=message,
            delivery_date=delivery_date
        )
        db.session.add(new_msg)
        db.session.commit()

        return jsonify({"message": "Message scheduled successfully!"}), 201

    except Exception as e:
        print("ERROR in /api/send-message:", e)
        return jsonify({"error": "Internal server error."}), 500

@app.get("/api/messages")
def list_messages():
    items = FutureMessage.query.order_by(FutureMessage.id.desc()).all()
    return jsonify([
        {
            "id": m.id,
            "email": m.email,
            "subject": m.subject,
            "message": m.message,
            "delivery_date": m.delivery_date.isoformat(),
            "sent": m.sent
        } for m in items
    ])

# --- Start app ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    start_scheduler(app)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
