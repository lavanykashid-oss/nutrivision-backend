from datetime import datetime
from app.config.database import db


class HealthAnalysis(db.Model):

    __tablename__ = "health_analysis"

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
        db.ForeignKey(
            "health_reports.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    health_score = db.Column(
        db.Integer,
        nullable=True
    )

    risk_level = db.Column(
        db.String(30),
        nullable=True
    )
    # Low
    # Moderate
    # High

    findings = db.Column(
        db.Text,
        nullable=True
    )

    deficiencies = db.Column(
        db.Text,
        nullable=True
    )

    recommendations = db.Column(
        db.Text,
        nullable=True
    )

    follow_up = db.Column(
        db.Text,
        nullable=True
    )

    ai_model = db.Column(
        db.String(100),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    report = db.relationship(
        "HealthReport",
        back_populates="analysis"
    )