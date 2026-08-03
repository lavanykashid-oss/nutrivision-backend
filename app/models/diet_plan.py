from datetime import datetime
from app.config.database import db


class DietPlan(db.Model):

    __tablename__ = "diet_plan"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    report_id = db.Column(
        db.Integer,
        db.ForeignKey("health_reports.id"),
        nullable=False,
        unique=True
    )

    breakfast = db.Column(
        db.Text,
        nullable=True
    )

    lunch = db.Column(
        db.Text,
        nullable=True
    )

    snack = db.Column(
        db.Text,
        nullable=True
    )

    dinner = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    report = db.relationship(
        "HealthReport",
        backref="diet_plan"
    )