from app.config.database import db
from app.models.health_report import HealthReport


class HealthReportRepository:

    @staticmethod
    def create(report):

        db.session.add(report)
        db.session.commit()

        return report

    @staticmethod
    def get(report_id):

        return HealthReport.query.get(report_id)

    @staticmethod
    def get_by_user(user_id):
        return HealthReport.query.filter_by(
            user_id=user_id
        ).order_by(
            HealthReport.created_at.desc()
        ).all()