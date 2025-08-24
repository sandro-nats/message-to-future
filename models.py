from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FutureMessage(db.Model):
    __tablename__ = "future_messages"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    sent = db.Column(db.Boolean, default=False)
