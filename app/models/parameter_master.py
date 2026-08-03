from datetime import datetime
from app.config.database import db


class ParameterMaster(db.Model):

    __tablename__ = "parameter_master"

    id = db.Column(db.Integer, primary_key=True)

    parameter_name = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    unit = db.Column(
        db.String(50),
        nullable=True
    )

    normal_min = db.Column(
        db.Float,
        nullable=True
    )

    normal_max = db.Column(
        db.Float,
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    deficiency_message = db.Column(
        db.Text,
        nullable=True
    )

    excess_message = db.Column(
        db.Text,
        nullable=True
    )

    recommendation = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    aliases = db.relationship(
    "ParameterAlias",
    back_populates="parameter",
    cascade="all, delete-orphan"
)