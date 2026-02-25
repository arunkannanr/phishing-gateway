from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PhishingLog(db.Model):
    __tablename__ = 'phishing_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_phishing = db.Column(db.Boolean, nullable=False)
    # Storing the specific reason (AI or Rule) for better auditing
    reason = db.Column(db.String(100)) 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.id} | Phishing: {self.is_phishing}>'