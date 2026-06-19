from app.config.database import db

class DeficiencyReport(db.Model):

    __tablename__ = "deficiency_reports"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    nutrient_name = db.Column(db.String(100))

    severity = db.Column(db.String(50))

    recommendation = db.Column(db.Text)

    report_date = db.Column(db.Date)