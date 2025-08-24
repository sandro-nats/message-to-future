from threading import Thread
from datetime import date
import time
from app import app, db
from models import FutureMessage

def send_due_messages():
    while True:
        today = date.today()
        with app.app_context():  # Ensures DB queries have application context
            messages = FutureMessage.query.filter_by(delivery_date=today, sent=False).all()
            for msg in messages:
                # Here you would normally send the email
                print(f"Sending message to {msg.email}: {msg.subject}")
                msg.sent = True
                db.session.commit()
        time.sleep(86400)  # Check once a day

def start_scheduler():
    thread = Thread(target=send_due_messages)
    thread.daemon = True
    thread.start()
