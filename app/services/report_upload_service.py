import os
import uuid

from werkzeug.utils import secure_filename

from app.models.health_report import HealthReport
from app.repositories.health_report_repository import HealthReportRepository


UPLOAD_FOLDER = "app/uploads/reports"


class ReportUploadService:

    @staticmethod
    def upload(file, user_id):

        filename = secure_filename(file.filename)

        unique_filename = f"{uuid.uuid4()}_{filename}"

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        file_path = os.path.join(
            UPLOAD_FOLDER,
            unique_filename
        )

        file.save(file_path)

        report = HealthReport(
            user_id=user_id,
            report_name=filename,
            report_type="CBC Report",
            file_path=file_path,
            status="uploaded"
        )

        HealthReportRepository.create(report)
        from app.services.health_report_service import HealthReportService

        HealthReportService.process_report(report)

        return report
    