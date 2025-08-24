import threading
import time
from datetime import datetime
from models import FutureMessage
from app import db

def check_messages():
    while True:
        now = datetime.utcnow().date()
        messages = FutureMessage.query.filter_by(sent=False, delivery_date=now).all()
        for msg in messages:
            print(f"[scheduler] Sending message to {msg.email}: {msg.subject}")
            msg.sent = True
            db.session.commit()
        time.sleep(60)  # check every minute

def start_scheduler():
    thread = threading.Thread(target=check_messages, daemon=True)
    thread.start()
    print("[scheduler] Email scheduler started.")
