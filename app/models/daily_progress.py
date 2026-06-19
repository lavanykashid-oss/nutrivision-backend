from app.config.database import db

class DailyProgress(db.Model):

    __tablename__ = "daily_progress"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    date = db.Column(db.Date)

    total_calories = db.Column(db.Float)

    total_protein = db.Column(db.Float)

    total_fat = db.Column(db.Float)

    total_carbs = db.Column(db.Float)