import re


class LocalResultExtractor:

    # ============================================================
    # NORMALIZE
    # ============================================================

    @staticmethod
    def normalize(text):

        if not text:
            return ""

        text = text.lower()

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
    # MAIN LOCAL EXTRACTION
    # ============================================================

    @staticmethod
    def extract(evidence, candidates):

        if not evidence or not candidates:

            return {}, candidates

        lines = [
            line.strip()
            for line in evidence.splitlines()
            if line.strip()
            and line.strip() != "---"
        ]

        extracted = {}

        resolved_ids = set()

        # ========================================================
        # ROW-FIRST PROCESSING
        #
        # Previously:
        #
        # candidate -> search every row
        #
        # Now:
        #
        # row -> determine BEST candidate
        #
        # This prevents:
        #
        # SGOT = 0.8 from SGOT/SGPT ratio
        # Lymphocytes = absolute lymphocyte count
        # RDW = RDW-SD
        # Creatinine = creatinine ratio
        # ========================================================

        for line in lines:

            normalized_line = (
                LocalResultExtractor.normalize(
                    line
                )
            )

            if not normalized_line:
                continue

            matches = []

            # ----------------------------------------------------
            # Find every candidate that could match this row
            # ----------------------------------------------------

            for candidate in candidates:

                candidate_aliases = []

                matched_alias = candidate.get(
                    "matched_alias"
                )

                if matched_alias:
                    candidate_aliases.append(
                        matched_alias
                    )

                name = candidate.get(
                    "name"
                )

                if name:
                    candidate_aliases.append(
                        name
                    )

                candidate_aliases = list(
                    set(candidate_aliases)
                )

                for alias in candidate_aliases:

                    normalized_alias = (
                        LocalResultExtractor.normalize(
                            alias
                        )
                    )

                    if not normalized_alias:
                        continue

                    # --------------------------------------------
                    # Alias must begin the laboratory row
                    # --------------------------------------------

                    if (
                        normalized_line
                        == normalized_alias

                        or normalized_line.startswith(
                            normalized_alias + " "
                        )
                    ):

                        matches.append({
                            "candidate":
                                candidate,

                            "alias":
                                alias,

                            "normalized_alias":
                                normalized_alias,

                            "length":
                                len(normalized_alias)
                        })

            if not matches:
                continue

            # ----------------------------------------------------
            # MOST SPECIFIC MATCH WINS
            #
            # Example:
            #
            # SGOT
            # SGOT SGPT Ratio
            #
            # SGOT SGPT Ratio wins.
            # ----------------------------------------------------

            matches.sort(
                key=lambda item:
                    item["length"],
                reverse=True
            )

            best_match = matches[0]

            candidate = best_match[
                "candidate"
            ]

            matched_alias = best_match[
                "alias"
            ]

            parameter_id = int(
                candidate["id"]
            )

            # Already resolved successfully.
            if parameter_id in resolved_ids:
                continue

            # ----------------------------------------------------
            # Extract value
            # ----------------------------------------------------

            result = (
                LocalResultExtractor.extract_from_line(
                    line,
                    matched_alias
                )
            )

            if not result:
                continue

            extracted[
                parameter_id
            ] = {

                "parameter_name":
                    candidate["name"],

                "parameter_id":
                    parameter_id,

                "value":
                    result["value"],

                "unit":
                    result.get("unit")
                    or candidate.get("unit"),

                "matched_alias":
                    matched_alias,

                "source":
                    "local"
            }

            resolved_ids.add(
                parameter_id
            )

        # ========================================================
        # UNRESOLVED PARAMETERS
        # ========================================================

        unresolved = []

        for candidate in candidates:

            parameter_id = int(
                candidate["id"]
            )

            if parameter_id not in resolved_ids:

                unresolved.append(
                    candidate
                )

        return extracted, unresolved

    # ============================================================
    # EXTRACT VALUE FROM A SINGLE RESULT ROW
    # ============================================================

    @staticmethod
    def extract_from_line(
        line,
        matched_alias
    ):

        if not line:
            return None

        lower = line.lower()

        # --------------------------------------------------------
        # Ignore obvious non-result rows
        # --------------------------------------------------------

        blocked_words = (
            "reference range",
            "normal range",
            "clinical significance",
            "sample collected",
            "sample received",
            "report released",
            "sample type",
            "available",
            "test asked",
            "clinically tested",
            "please correlate",
            "derived from"
        )

        if any(
            blocked in lower
            for blocked in blocked_words
        ):
            return None

        if lower.startswith(
            "method"
        ):
            return None

        # --------------------------------------------------------
        # Remove matched test name from START only
        # --------------------------------------------------------

        pattern = re.compile(
            r"^\s*"
            + re.escape(
                matched_alias
            ),
            re.IGNORECASE
        )

        working_line = pattern.sub(
            "",
            line,
            count=1
        ).strip()

        # --------------------------------------------------------
        # Extract first numeric value
        # --------------------------------------------------------

        numbers = re.findall(
            r"(?<![A-Za-z])"
            r"[-+]?\d+(?:\.\d+)?",
            working_line
        )

        if not numbers:
            return None

        try:

            value = float(
                numbers[0]
            )

        except ValueError:

            return None

        # --------------------------------------------------------
        # Detect unit
        #
        # IMPORTANT:
        # Specific units must be before generic ones.
        # --------------------------------------------------------

        unit_patterns = [

            r"mL/min/1\.73\s*m(?:2|²)",

            r"X\s*10[³3]\s*/\s*µL",
            r"X\s*10\^?6\s*/\s*µL",

            r"million/cumm",

            r"Cells/ul",

            r"/HPF",
            r"/LPF",

            r"µIU/ml",
            r"uIU/ml",

            r"µg/dl",
            r"ug/dl",

            r"ng/dl",
            r"ng/ml",

            r"pg/ml",

            r"mg/dl",
            r"mg/l",

            r"gm/dl",
            r"g/dl",

            r"U/L",

            r"fL",

            r"pg",

            r"%",

            r"Ratio",

            r"\bmL\b"
        ]

        unit = None

        for unit_pattern in unit_patterns:

            match = re.search(
                unit_pattern,
                working_line,
                re.IGNORECASE
            )

            if match:

                unit = match.group(
                    0
                )

                break

        return {
            "value": value,
            "unit": unit
        }