from datetime import datetime
from app.config.database import db

class Meal(db.Model):

    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    meal_name = db.Column(
        db.String(150),
        nullable=False
    )

    image_url = db.Column(db.Text)

    meal_type = db.Column(db.String(50))

    meal_date = db.Column(db.Date)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )