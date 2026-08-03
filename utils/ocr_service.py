import os
import fitz
from PIL import Image


class OCRService:

    @staticmethod
    def extract_text(file_path):
        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return OCRService.extract_pdf(file_path)

        return OCRService.extract_image(file_path)

    @staticmethod
    def extract_image(file_path):
        raise NotImplementedError(
            "Image OCR is disabled. Use Gemini Vision for images."
        )

    @staticmethod
    def extract_pdf(file_path):

        doc = fitz.open(file_path)

        text = ""

        for page in doc:
            text += page.get_text("text")
            text += "\n"

        doc.close()

        return text.strip()