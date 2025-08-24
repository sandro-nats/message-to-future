from models import FutureMessage
from app import db
import datetime
import threading
import time

def check_messages():
    while True:
        today = datetime.date.today()
        messages = FutureMessage.query.filter_by(sent=False).all()
        for msg in messages:
            if msg.delivery_date <= today:
                print(f"Sending message to {msg.email}: {msg.subject}")
                # Here you would integrate actual email sending
                msg.sent = True
                db.session.commit()
        time.sleep(60)  # Check every minute

def start_scheduler():
    thread = threading.Thread(target=check_messages)
    thread.daemon = True  # So it stops when the app stops
    thread.start()
    print("Scheduler started")
