from datetime import datetime
from app.config.database import db


class ParameterAlias(db.Model):

    __tablename__ = "parameter_alias"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    parameter_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "parameter_master.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    alias = db.Column(
        db.String(150),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    parameter = db.relationship(
        "ParameterMaster",
        back_populates="aliases"
    )