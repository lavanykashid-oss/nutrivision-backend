from datetime import datetime
from app.config.database import db

class ChatMessage(db.Model):

    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user_message = db.Column(db.Text)

    ai_response = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )