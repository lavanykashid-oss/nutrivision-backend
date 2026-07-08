from app.config.database import db

class UserGoal(db.Model):

    __tablename__ = "user_goals"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    goal_type = db.Column(db.String(50))

   