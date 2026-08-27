import re


class EvidenceExtractor:

    # ============================================================
    # NORMALIZE TEXT FOR PARAMETER MATCHING
    # ============================================================

    @staticmethod
    def normalize_for_match(text):

        if not text:
            return ""

        text = text.lower()

        # Ignore punctuation differences:
        #
        # Transferrin Saturation %
        # % TRANSFERRIN SATURATION
        #
        # SGOT / SGPT
        # SGOT-SGPT
        #
        # become comparable strings.
        text = re.sub(
            r"[^a-z0-9]+",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ============================================================
    # NOISE DETECTION
    # ============================================================

    @staticmethod
    def is_noise_line(line):

        if not line:
            return True

        lower = line.lower().strip()

        # --------------------------------------------------------
        # Exact / prefix noise
        # --------------------------------------------------------

        noise_prefixes = (
            "sample collected",
            "sample received",
            "report released",
            "sample type",
            "labcode",
            "barcode",
            "clinically tested",
            "please correlate",
            "note :",
            "note:",
            "method :",
            "method:",
            "specifications:",
            "specification:",
            "clinical significance",
            "reference:",
            "references:",
            "alert !!!",
            "alert:",
            "comments :",
            "comments:",
            "comment :",
            "comment:",
            "~~ end of report",
        )

        if lower.startswith(
            noise_prefixes
        ):
            return True

        # --------------------------------------------------------
        # Index-page rows
        # --------------------------------------------------------

        if lower.endswith("available"):
            return True

        # --------------------------------------------------------
        # Narrative paragraphs
        # --------------------------------------------------------

        narrative_phrases = (
            "for diagnostic purpose",
            "results should always be assessed",
            "this test is used",
            "this device performs",
            "clinical examination",
            "medical history",
            "associated with",
            "it is recommended",
            "it cannot be measured",
            "approximately equates",
            "equation together with",
            "management of patients",
            "detection and management",
            "gold standard",
            "reference interval",
            "formation of myelin",
            "dietary deficiency",
            "increase in vitamin",
            "decrease in vitamin",
            "n engl j med",
            "ann intern med",
            "et al.",
        )

        if any(
            phrase in lower
            for phrase in narrative_phrases
        ):
            return True

        # --------------------------------------------------------
        # Method-description rows
        # --------------------------------------------------------

        method_keywords = (
            "oxidase",
            "esterase",
            "peroxidase",
            "ifcc",
            "enzymatic",
            "spectrophotometric",
            "colorimetric",
            "chemiluminescent",
            "chemi luminescent",
            "immuno assay",
            "fully automated",
            "arsenazo",
            "biuret method",
            "bcg method",
            "kinetic uv",
        )

        if any(
            keyword in lower
            for keyword in method_keywords
        ):

            # Preserve genuine result rows even if the
            # technology/method happens to be on same line.
            if not EvidenceExtractor.looks_like_result_row(
                line
            ):
                return True

        return False

    # ============================================================
    # RESULT ROW DETECTION
    # ============================================================

    @staticmethod
    def looks_like_result_row(line):

        if not line:
            return False

        lower = line.lower()

        # --------------------------------------------------------
        # Qualitative results
        # --------------------------------------------------------

        qualitative_values = (
            "absent",
            "present",
            "positive",
            "negative",
            "clear",
            "nil",
            "trace",
            "pale yellow",
        )

        if any(
            value in lower
            for value in qualitative_values
        ):
            return True

        # --------------------------------------------------------
        # Common laboratory units
        # --------------------------------------------------------

        unit_pattern = (
            r"(?:"
            r"mg/dl|"
            r"mg/l|"
            r"µg/dl|"
            r"ug/dl|"
            r"ng/dl|"
            r"ng/ml|"
            r"pg/ml|"
            r"g/dl|"
            r"gm/dl|"
            r"µiu/ml|"
            r"uiu/ml|"
            r"u/l|"
            r"fl|"
            r"pg|"
            r"%|"
            r"ratio|"
            r"ml/min/1\.73|"
            r"x\s*10[³3]|"
            r"million/cumm|"
            r"/hpf|"
            r"/lpf"
            r")"
        )

        if re.search(
            unit_pattern,
            lower,
            re.IGNORECASE
        ):
            return True

        return False

    # ============================================================
    # DOES BLOCK CONTAIN A RESULT?
    # ============================================================

    @staticmethod
    def has_result_value(block):

        if not block:
            return False

        # --------------------------------------------------------
        # Numeric values
        # --------------------------------------------------------

        if re.search(
            r"(?<![A-Za-z])"
            r"[-+]?\d+(?:\.\d+)?",
            block
        ):
            return True

        # --------------------------------------------------------
        # Qualitative values
        # --------------------------------------------------------

        qualitative_values = (
            "absent",
            "present",
            "positive",
            "negative",
            "clear",
            "nil",
            "trace",
            "pale yellow",
        )

        lower = block.lower()

        return any(
            value in lower
            for value in qualitative_values
        )

    # ============================================================
    # MAIN EXTRACTION
    # ============================================================

    @staticmethod
    def extract(
        text,
        candidates,
        lines_before=1,
        lines_after=3
    ):

        if not text or not candidates:
            return ""

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return ""

        ranges = []

        # ========================================================
        # FIND EVERY PARAMETER OCCURRENCE
        # ========================================================

        for candidate in candidates:

            search_terms = []

            matched_alias = candidate.get(
                "matched_alias"
            )

            parameter_name = candidate.get(
                "name"
            )

            if matched_alias:
                search_terms.append(
                    matched_alias
                )

            if (
                parameter_name
                and parameter_name
                not in search_terms
            ):
                search_terms.append(
                    parameter_name
                )

            # ----------------------------------------------------
            # Normalize candidate names / aliases
            # ----------------------------------------------------

            normalized_terms = []

            for term in search_terms:

                normalized_term = (
                    EvidenceExtractor
                    .normalize_for_match(
                        term
                    )
                )

                if not normalized_term:
                    continue

                # Avoid dangerous tiny normalized aliases.
                if len(normalized_term) < 3:
                    continue

                normalized_terms.append(
                    normalized_term
                )

            if not normalized_terms:
                continue

            # ----------------------------------------------------
            # Search every OCR line
            # ----------------------------------------------------

            for index, line in enumerate(
                lines
            ):

                normalized_line = (
                    EvidenceExtractor
                    .normalize_for_match(
                        line
                    )
                )

                if not normalized_line:
                    continue

                matched = False

                for normalized_term in (
                    normalized_terms
                ):

                    if (
                        normalized_term
                        in normalized_line
                    ):

                        matched = True
                        break

                if not matched:
                    continue

                # ================================================
                # IMPORTANT:
                # THESE LINES MUST REMAIN INSIDE THIS LOOP.
                # ================================================

                start = max(
                    0,
                    index - lines_before
                )

                end = min(
                    len(lines),
                    index + lines_after + 1
                )

                ranges.append(
                    (
                        start,
                        end
                    )
                )

        # --------------------------------------------------------
        # Nothing matched
        # --------------------------------------------------------

        if not ranges:
            return ""

        # ========================================================
        # MERGE OVERLAPPING / NEIGHBOURING RANGES
        # ========================================================

        ranges.sort(
            key=lambda item: item[0]
        )

        merged_ranges = []

        current_start, current_end = (
            ranges[0]
        )

        for start, end in ranges[1:]:

            if start <= current_end + 1:

                current_end = max(
                    current_end,
                    end
                )

            else:

                merged_ranges.append(
                    (
                        current_start,
                        current_end
                    )
                )

                current_start = start
                current_end = end

        merged_ranges.append(
            (
                current_start,
                current_end
            )
        )

        # ========================================================
        # BUILD CLEAN EVIDENCE
        # ========================================================

        blocks = []

        for start, end in merged_ranges:

            block_lines = []

            for line in lines[
                start:end
            ]:

                if (
                    EvidenceExtractor
                    .is_noise_line(
                        line
                    )
                ):
                    continue

                block_lines.append(
                    line
                )

            block = "\n".join(
                block_lines
            ).strip()

            if not block:
                continue

            if not (
                EvidenceExtractor
                .has_result_value(
                    block
                )
            ):
                continue

            blocks.append(
                block
            )

        return "\n\n---\n\n".join(
            blocks
        )