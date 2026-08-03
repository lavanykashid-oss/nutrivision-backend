from app import create_app
from app.models.health_report import HealthReport
from app.services.health_report_service import HealthReportService

app = create_app()

with app.app_context():

    report = HealthReport.query.first()

    if not report:
        print("No reports found.")
    else:
        HealthReportService.process_report(report)