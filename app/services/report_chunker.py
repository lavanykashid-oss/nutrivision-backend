# import re


# class ReportChunker:

#     @staticmethod
#     def split_text(text, max_chars=12000):

#         if not text:
#             return []

#         # Try to preserve page boundaries if present
#         pages = re.split(
#             r"\n\s*(?:PAGE\s*\d+(?:\s*OF\s*\d+)?)\s*\n",
#             text,
#             flags=re.IGNORECASE
#         )

#         chunks = []

#         for page in pages:

#             page = page.strip()

#             if not page:
#                 continue

#             if len(page) <= max_chars:

#                 chunks.append(page)

#                 continue

#             # Further divide large pages
#             start = 0

#             while start < len(page):

#                 end = start + max_chars

#                 chunk = page[start:end]

#                 chunks.append(
#                     chunk
#                 )

#                 start = end

#         return chunks


# import re


# class ReportChunker:

#     @staticmethod
#     def split_text(text, max_chars=12000):

#         if not text:
#             return []

#         # --------------------------------------------------------
#         # Split using our OCRService page markers
#         #
#         # Supports:
#         # ===== PAGE 1 =====
#         # PAGE 1 OF 12
#         # Page : 1 of 12
#         # --------------------------------------------------------

#         page_pattern = re.compile(
#             r"""
#             (?:={2,}\s*PAGE\s+\d+\s*={2,})
#             |
#             (?:PAGE\s*:?\s*\d+\s+(?:OF|/)\s*\d+)
#             """,
#             re.IGNORECASE | re.VERBOSE
#         )

#         pages = page_pattern.split(text)

#         chunks = []

#         for page in pages:

#             page = page.strip()

#             if not page:
#                 continue

#             # Normal page fits within limit
#             if len(page) <= max_chars:
#                 chunks.append(page)
#                 continue

#             # ----------------------------------------------------
#             # Very large page:
#             # split safely by lines instead of cutting characters
#             # in the middle of a laboratory result.
#             # ----------------------------------------------------

#             lines = page.splitlines()

#             current_chunk = []
#             current_length = 0

#             for line in lines:

#                 line_length = len(line) + 1

#                 if (
#                     current_chunk
#                     and
#                     current_length + line_length > max_chars
#                 ):

#                     chunks.append(
#                         "\n".join(current_chunk)
#                     )

#                     current_chunk = []
#                     current_length = 0

#                 current_chunk.append(line)

#                 current_length += line_length

#             if current_chunk:

#                 chunks.append(
#                     "\n".join(current_chunk)
#                 )

#         return chunks



import re


class ReportChunker:

    @staticmethod
    def split_text(text, max_chars=12000):

        if not text:
            return []

        # ========================================================
        # PRIMARY SPLIT
        #
        # OCRService itself creates markers like:
        #
        # ===== PAGE 1 =====
        # ===== PAGE 2 =====
        #
        # We trust ONLY these markers.
        #
        # Do NOT split using text printed inside the report such as:
        # "Page : 1 of 14"
        # because that creates duplicate chunks.
        # ========================================================

        page_pattern = re.compile(
            r"={3,}\s*PAGE\s+\d+\s*={3,}",
            re.IGNORECASE
        )

        pages = page_pattern.split(text)

        chunks = []

        for page in pages:

            page = page.strip()

            if not page:
                continue

            # ----------------------------------------------------
            # Normal physical page
            # ----------------------------------------------------

            if len(page) <= max_chars:

                chunks.append(page)

                continue

            # ----------------------------------------------------
            # Safety fallback:
            # If one physical page is extremely large,
            # split it by complete lines.
            #
            # Never cut blindly in the middle of a line/value.
            # ----------------------------------------------------

            lines = page.splitlines()

            current_chunk = []
            current_length = 0

            for line in lines:

                line_length = len(line) + 1

                if (
                    current_chunk
                    and
                    current_length + line_length > max_chars
                ):

                    chunks.append(
                        "\n".join(current_chunk)
                    )

                    current_chunk = []
                    current_length = 0

                current_chunk.append(line)

                current_length += line_length

            if current_chunk:

                chunks.append(
                    "\n".join(current_chunk)
                )

        return chunks