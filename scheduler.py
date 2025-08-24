import os
import time
import threading
from datetime import date
import smtplib
from email.mime.text import MIMEText
from models import FutureMessage, db

def send_email(to_email: str, subject: str, message: str) -> None:
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT_SSL", "465"))

    if not sender_email or not sender_password:
        print("[scheduler] Missing SENDER_EMAIL or SENDER_PASSWORD; skipping send.")
        return

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

def email_scheduler(app):
    with app.app_context():
        print("[scheduler] Email scheduler started.")
        while True:
            try:
                today = date.today()
                to_send = FutureMessage.query.filter_by(delivery_date=today, sent=False).all()
                if to_send:
                    print(f"[scheduler] Sending {len(to_send)} message(s) for {today.isoformat()}")
                for msg in to_send:
                    try:
                        send_email(msg.email, msg.subject, msg.message)
                        msg.sent = True
                        db.session.commit()
                        print(f"[scheduler] Sent message id={msg.id} to {msg.email}")
                    except Exception as e:
                        db.session.rollback()
                        print(f"[scheduler] Failed message id={msg.id}: {e}")
            except Exception as outer:
                print("[scheduler] Unhandled scheduler error:", outer)
            time.sleep(3600)

def start_scheduler(app):
    thread = threading.Thread(target=email_scheduler, args=(app,))
    thread.daemon = True
    thread.start()
