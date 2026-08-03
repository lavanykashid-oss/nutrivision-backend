from datetime import datetime
from app.config.database import db


class HealthReport(db.Model):

    __tablename__ = "health_reports"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    report_name = db.Column(
        db.String(255),
        nullable=False
    )

    report_type = db.Column(
        db.String(50),
        nullable=False
    )

    patient_name = db.Column(
    db.String(255),
    nullable=True
)

    age = db.Column(
    db.String(50),
    nullable=True
)

    gender = db.Column(
    db.String(20),
    nullable=True
)

    laboratory = db.Column(
    db.String(255),
    nullable=True
)

    referred_by = db.Column(
    db.String(255),
    nullable=True
)

    

    file_path = db.Column(
        db.String(500),
        nullable=False
    )

    ocr_text = db.Column(
        db.Text,
        nullable=True
    )

    report_date = db.Column(
        db.Date,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="uploaded"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="health_reports"
    )

    parameters = db.relationship(
        "HealthParameter",
        back_populates="report",
        cascade="all, delete-orphan"
    )
    

    analysis = db.relationship(
        "HealthAnalysis",
        back_populates="report",
        uselist=False,
        cascade="all, delete-orphan"
    )