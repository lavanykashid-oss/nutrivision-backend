from utils.ocr_service import OCRService
from utils.report_parser import ReportParser


text = OCRService.extract_text(
    "uploads/health_reports/sample.pdf"
)

data = ReportParser.extract_parameters(text)

print(data)