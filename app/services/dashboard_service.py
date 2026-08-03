from app.models.health_report import HealthReport
from app.models.health_analysis import HealthAnalysis


class DashboardService:

    @staticmethod
    def get_dashboard(user_id):

        latest_report = (
            HealthReport.query
            .filter_by(user_id=user_id)
            .order_by(HealthReport.created_at.desc())
            .first()
        )

        if not latest_report:

            return None

        analysis = latest_report.analysis

        return {
            "latest_report": latest_report,
            "analysis": analysis
        }