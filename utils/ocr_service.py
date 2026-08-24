# import os
# import fitz
# from PIL import Image


# class OCRService:

#     @staticmethod
#     def extract_text(file_path):
#         extension = os.path.splitext(file_path)[1].lower()

#         if extension == ".pdf":
#             return OCRService.extract_pdf(file_path)

#         return OCRService.extract_image(file_path)

#     @staticmethod
#     def extract_image(file_path):
#         raise NotImplementedError(
#             "Image OCR is disabled. Use Gemini Vision for images."
#         )

#     @staticmethod
#     def extract_pdf(file_path):

#         doc = fitz.open(file_path)

#         text = ""

#         for page in doc:
#             text += page.get_text("text")
#             text += "\n"

#         doc.close()

#         return text.strip()














import os
import fitz


class OCRService:

    @staticmethod
    def extract_text(file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return OCRService.extract_pdf(file_path)

        return OCRService.extract_image(file_path)

    # ============================================================
    # IMAGE
    # ============================================================

    @staticmethod
    def extract_image(file_path):

        raise NotImplementedError(
            "Image OCR is disabled. Use Gemini Vision for images."
        )

    # ============================================================
    # PDF
    # ============================================================

    @staticmethod
    def extract_pdf(file_path):

        doc = fitz.open(file_path)

        pages = []

        print("=" * 80)
        print("OCR SERVICE")
        print(f"PDF: {file_path}")
        print(f"TOTAL PAGES: {len(doc)}")
        print("=" * 80)

        for page_number, page in enumerate(doc, start=1):

            print(
                f"Processing page {page_number}/{len(doc)}"
            )

            # ----------------------------------------------------
            # First try normal PDF text extraction
            # ----------------------------------------------------

            text = page.get_text(
                "text",
                sort=True
            ).strip()

            # ----------------------------------------------------
            # If page has little/no text, use OCR
            # ----------------------------------------------------

            if len(text) < 50:

                print(
                    f"Page {page_number}: "
                    f"normal text insufficient -> OCR"
                )

                try:

                    text_page = page.get_textpage_ocr(
                        language="eng",
                        dpi=200,
                        full=True
                    )

                    text = page.get_text(
                        "text",
                        textpage=text_page,
                        sort=True
                    ).strip()

                except Exception as e:

                    print(
                        f"OCR failed on page "
                        f"{page_number}: {e}"
                    )

                    text = ""

            else:

                print(
                    f"Page {page_number}: "
                    f"normal PDF text used"
                )

            # ----------------------------------------------------
            # Keep page boundary
            # ----------------------------------------------------

            pages.append(
                f"\n===== PAGE {page_number} =====\n"
                f"{text}\n"
            )

        doc.close()

        final_text = "\n".join(pages).strip()

        print("=" * 80)
        print("OCR COMPLETE")
        print(f"TOTAL CHARACTERS: {len(final_text)}")
        print("=" * 80)

        return final_text