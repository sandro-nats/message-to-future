import threading
import time
from datetime import date
from app import app, db, FutureMessage
from email_utils import send_email

def send_due_messages():
    with app.app_context():  # ✅ fixes application context issue
        while True:
            today = date.today()
            messages = FutureMessage.query.filter_by(delivery_date=today, sent=False).all()
            
            for msg in messages:
                send_email(msg.email, msg.subject, msg.message)
                msg.sent = True
                db.session.commit()
            
            time.sleep(60)  # check once per minute

def start_scheduler():
    t = threading.Thread(target=send_due_messages, daemon=True)
    t.start()
