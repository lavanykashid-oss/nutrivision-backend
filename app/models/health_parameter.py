from datetime import datetime
from app.config.database import db


class HealthParameter(db.Model):

    __tablename__ = "health_parameters"

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
        nullable=False
    )

    parameter_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "parameter_master.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    value = db.Column(
        db.Float,
        nullable=True
    )

    unit = db.Column(
        db.String(50),
        nullable=True
    )

    reference_low = db.Column(
        db.Float,
        nullable=True
    )

    reference_high = db.Column(
        db.Float,
        nullable=True
    )

    flag = db.Column(
        db.String(20),
        nullable=True
    )
    # Normal
    # High
    # Low
    # Critical

    raw_text = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    report = db.relationship(
        "HealthReport",
        back_populates="parameters"
    )

    parameter = db.relationship(
        "ParameterMaster"
    )