from datetime import datetime
from app.config.database import db


class ChatMessage(db.Model):

    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("chat_sessions.id"),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )