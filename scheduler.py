from threading import Thread
import time
from datetime import date
from models import FutureMessage
from app import db

def send_due_messages():
    while True:
        today = date.today()
        messages = FutureMessage.query.filter_by(delivery_date=today, sent=False).all()
        for msg in messages:
            # Here you can send email via SMTP or another service
            print(f"Sending message to {msg.email}: {msg.message}")
            msg.sent = True
            db.session.commit()
        time.sleep(86400)  # Check once per day

def start_scheduler():
    thread = Thread(target=send_due_messages)
    thread.daemon = True
    thread.start()
