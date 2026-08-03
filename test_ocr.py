# import os

# print("Current directory:")
# print(os.getcwd())

# pdf_path = os.path.abspath("uploads/health_reports/sample.pdf")

# print("PDF path:")
# print(pdf_path)

# print("Exists?")
# print(os.path.exists(pdf_path))

import os
from utils.ocr_service import OCRService

pdf_path = "uploads/health_reports/sample.pdf"

print(os.path.exists(pdf_path))

text = OCRService.extract_text(pdf_path)

print(text[:3000])