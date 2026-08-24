# import re

# from app.models.parameter_alias import ParameterAlias


# class ReportParser:

#     # ============================================================
#     # MAIN REPORT PARSER
#     # ============================================================

#     @staticmethod
#     def parse_report(text: str):

#         metadata = {}

#         # --------------------------------------------------------
#         # Patient Name
#         # --------------------------------------------------------

#         metadata["patient_name"] = None

#         match = re.search(
#             r"Patient\s*Name\s*[:\-]?\s*([^\n]+)",
#             text,
#             re.IGNORECASE
#         )

#         if match:
#             metadata["patient_name"] = match.group(1).strip()

#         # Fallback
#         if metadata["patient_name"] is None:

#             fallback = re.search(
#                 r"Dr\.\s*Payal\s*Shah[\s\S]*?\n"
#                 r"([A-Za-z. ]+)\n\s*Age\s*:",
#                 text,
#                 re.IGNORECASE
#             )

#             if fallback:
#                 metadata["patient_name"] = fallback.group(1).strip()

#         # --------------------------------------------------------
#         # Age
#         # --------------------------------------------------------

#         age = re.search(
#             r"Age\s*:\s*(\d+)\s*Years?",
#             text,
#             re.IGNORECASE
#         )

#         metadata["age"] = age.group(1).strip() if age else None

#         # --------------------------------------------------------
#         # Gender
#         # --------------------------------------------------------

#         gender = re.search(
#             r"Sex\s*:\s*(Male|Female)",
#             text,
#             re.IGNORECASE
#         )

#         metadata["gender"] = (
#             gender.group(1).title()
#             if gender
#             else None
#         )

#         # --------------------------------------------------------
#         # Laboratory
#         # --------------------------------------------------------

#         lab = re.search(
#             r"^(.*?)\n",
#             text,
#             re.MULTILINE
#         )

#         metadata["laboratory"] = (
#             lab.group(1).strip()
#             if lab
#             else None
#         )

#         # --------------------------------------------------------
#         # Referred By
#         # --------------------------------------------------------

#         doctor = re.search(
#             r"Ref\.?\s*By\s*:\s*([^\n]+)",
#             text,
#             re.IGNORECASE
#         )

#         metadata["referred_by"] = (
#             doctor.group(1).strip()
#             if doctor
#             else None
#         )

#         # --------------------------------------------------------
#         # Report Date
#         # --------------------------------------------------------

#         metadata["report_date"] = None

#         match = re.search(
#             r"(\d{2}[/-]\d{2}[/-]\d{4})",
#             text
#         )

#         if match:
#             metadata["report_date"] = match.group(1)

#         # --------------------------------------------------------
#         # Extract Parameters
#         # --------------------------------------------------------

#         parameters = ReportParser.extract_parameters(text)

#         return {
#             "metadata": metadata,
#             "parameters": parameters
#         }

#     # ============================================================
#     # PARAMETER EXTRACTION
#     # ============================================================

#     @staticmethod
#     def extract_parameters(text):

#         parameters = {}

#         # ========================================================
#         # LOAD ALIASES
#         # ========================================================

#         aliases = ParameterAlias.query.all()

#         alias_items = []

#         for alias_object in aliases:

#             if not alias_object.parameter:
#                 continue

#             alias = re.sub(
#                 r"\s+",
#                 " ",
#                 alias_object.alias.lower().strip()
#             )

#             if not alias:
#                 continue

#             alias_items.append(
#                 {
#                     "alias": alias,
#                     "parameter_id": alias_object.parameter.id,
#                     "parameter_name": (
#                         alias_object.parameter.parameter_name
#                     )
#                 }
#             )

#         # ========================================================
#         # LONGEST ALIAS FIRST
#         # ========================================================

#         alias_items.sort(
#             key=lambda x: len(x["alias"]),
#             reverse=True
#         )

#         # ========================================================
#         # NORMALIZE OCR TEXT
#         # ========================================================

#         lines = []

#         for raw_line in text.splitlines():

#             line = re.sub(
#                 r"\s+",
#                 " ",
#                 raw_line
#             ).strip()

#             if line:
#                 lines.append(line)

#         # ========================================================
#         # CONSTANTS
#         # ========================================================

#         QUALITATIVE_VALUES = {
#             "absent",
#             "present",
#             "nil",
#             "negative",
#             "positive",
#             "normal",
#             "trace",
#             "few",
#             "occasional",
#             "none",
#         }

#         UNIT_PATTERNS = [
#             "%",
#             "mg/dl",
#             "mg/l",
#             "g/dl",
#             "gm/dl",
#             "u/l",
#             "ng/dl",
#             "µg/dl",
#             "ug/dl",
#             "µiu/ml",
#             "uiu/ml",
#             "ratio",
#             "ml",
#             "fl",
#             "pg",
#             "pq",
#             "cells/ul",
#             "cells/ul*",
#             "cells / ul",
#             "cells / hp",
#             "x 10",
#             "x 10³",
#             "x 10^3",
#             "x 10^6",
#         ]

#         METHOD_PATTERNS = [
#             "photometry",
#             "calculated",
#             "c.l.i.a",
#             "clia",
#             "h.p.l.c",
#             "hplc",
#             "chemiluminescent",
#             "immuno assay",
#             "immunoassay",
#             "derived",
#             "kinetic",
#             "enzymatic",
#             "colorimetric",
#             "spectrophotometry",
#             "microscopy",
#             "dipstick",
#             "fully automated",
#             "flow cytometry",
#             "hydrodynamic focussing",
#             "sls-hemoglobin",
#         ]

#         HEADER_PATTERNS = {
#             "test name",
#             "technology",
#             "value",
#             "units",
#             "reference range",
#             "reference value",
#             "investigation",
#             "result",
#             "method",
#             "remarks",
#             "sample type",
#             "barcode",
#             "labcode",
#             "page",
#             "name",
#             "self",
#             "ref. by",
#             "test asked",
#         }

#         # ========================================================
#         # HELPERS
#         # ========================================================

#         def normalize(line):

#             return re.sub(
#                 r"\s+",
#                 " ",
#                 line.lower().strip()
#             )

#         # --------------------------------------------------------
#         # Is Unit
#         # --------------------------------------------------------

#         def is_unit(line):

#             lower = normalize(line)

#             return any(
#                 unit in lower
#                 for unit in UNIT_PATTERNS
#             )

#         # --------------------------------------------------------
#         # Is Method
#         # --------------------------------------------------------

#         def is_method(line):

#             lower = normalize(line)

#             return any(
#                 method in lower
#                 for method in METHOD_PATTERNS
#             )

#         # --------------------------------------------------------
#         # Is Header
#         # --------------------------------------------------------

#         def is_header(line):

#             return normalize(line) in HEADER_PATTERNS

#         # --------------------------------------------------------
#         # Reference Range
#         # --------------------------------------------------------

#         def is_reference_range(line):

#             line = line.strip()

#             patterns = [

#                 r"^\d+(?:\.\d+)?\s*[-–]\s*\d+(?:\.\d+)?$",

#                 r"^<\s*\d+(?:\.\d+)?$",

#                 r">\s*\d+(?:\.\d+)?",

#                 r"^<=\s*\d+(?:\.\d+)?$",

#                 r"^>=\s*\d+(?:\.\d+)?$",

#                 r"^\d+(?:\.\d+)?%\s*[-–]\s*"
#                 r"\d+(?:\.\d+)?%?$",

#                 r"^\d+(?:\.\d+)?\s*[-–]\s*"
#                 r"\d+(?:\.\d+)?\s*[a-zµ/0-9*]+$",

#                 r"^(male|female)\s*:",
#             ]

#             return any(
#                 re.fullmatch(
#                     pattern,
#                     line,
#                     re.IGNORECASE
#                 )
#                 for pattern in patterns
#             )

#         # --------------------------------------------------------
#         # Extract Value
#         # --------------------------------------------------------

#         def extract_value(line):

#             line = line.strip()

#             if not line:
#                 return None

#             # Qualitative result
#             if line.lower() in QUALITATIVE_VALUES:
#                 return None

#             # Reference range
#             if is_reference_range(line):
#                 return None

#             # Unit
#             if is_unit(line):
#                 return None

#             # Method
#             if is_method(line):
#                 return None

#             # Pure number
#             match = re.fullmatch(
#                 r"[-+]?\d+(?:\.\d+)?%?",
#                 line
#             )

#             if match:

#                 try:
#                     return float(
#                         match.group().replace("%", "")
#                     )
#                 except ValueError:
#                     return None

#             # Number + unit
#             match = re.fullmatch(
#                 r"([-+]?\d+(?:\.\d+)?)\s*"
#                 r"(?:mg/dl|mg/l|g/dl|gm/dl|u/l|ng/dl|"
#                 r"µg/dl|ug/dl|µiu/ml|uiu/ml|%)",
#                 line,
#                 re.IGNORECASE
#             )

#             if match:

#                 try:
#                     return float(match.group(1))
#                 except ValueError:
#                     return None

#             return None

#         # ========================================================
#         # FIND PARAMETER
#         # ========================================================

#         def find_parameter(line):

#             lower = normalize(line)

#             if is_header(lower):
#                 return None

#             if is_method(lower):
#                 return None

#             if is_unit(lower):
#                 return None

#             if is_reference_range(lower):
#                 return None

#             if len(lower) > 100:
#                 return None

#             sentence_words = [
#                 "please correlate",
#                 "diagnostic purpose",
#                 "known diabetics",
#                 "guidance",
#                 "specifications",
#                 "sensitivity",
#                 "precision",
#                 "kit validation",
#                 "clinically tested",
#                 "underlined values",
#                 "note:-",
#                 "note:",
#             ]

#             if any(
#                 word in lower
#                 for word in sentence_words
#             ):
#                 return None

#             # ----------------------------------------------------
#             # Search aliases
#             # ----------------------------------------------------

#             for item in alias_items:

#                 alias = item["alias"]

#                 pattern = (
#                     r"(?<![a-z0-9])"
#                     + re.escape(alias)
#                     + r"(?![a-z0-9])"
#                 )

#                 if re.search(
#                     pattern,
#                     lower
#                 ):

#                     return item

#             return None

#         # ========================================================
#         # BUILD PARAMETER INDEX
#         # ========================================================

#         parameter_lines = []

#         for index, line in enumerate(lines):

#             match = find_parameter(line)

#             if match:

#                 parameter_lines.append(
#                     (
#                         index,
#                         match
#                     )
#                 )

#         # ========================================================
#         # DEBUG
#         # ========================================================

#         print(
#             "\n========== PARSER START ==========\n"
#         )

#         # ========================================================
#         # PROCESS PARAMETERS
#         # ========================================================

#         for position, (
#             i,
#             parameter_info
#         ) in enumerate(parameter_lines):

#             parameter_id = parameter_info["parameter_id"]

#             parameter_name = parameter_info[
#                 "parameter_name"
#             ]

#             alias = parameter_info["alias"]

#             # ----------------------------------------------------
#             # Avoid duplicate parameter IDs
#             # ----------------------------------------------------

#             if parameter_id in parameters:
#                 continue

#             print(
#                 f"\nSearching value for: {parameter_name}"
#             )

#             print(
#                 f"Matched alias: {alias}"
#             )

#             print(
#                 f"Parameter line: {lines[i]}"
#             )

#             value = None

#             # ----------------------------------------------------
#             # Boundaries
#             # ----------------------------------------------------

#             previous_parameter_index = -1

#             next_parameter_index = len(lines)

#             if position > 0:

#                 previous_parameter_index = (
#                     parameter_lines[position - 1][0]
#                 )

#             if position < len(parameter_lines) - 1:

#                 next_parameter_index = (
#                     parameter_lines[position + 1][0]
#                 )

#             # ====================================================
#             # STRATEGY 1
#             # SAME LINE
#             # ====================================================

#             same_line = lines[i]

#             alias_start = same_line.lower().find(alias)

#             if alias_start != -1:

#                 remaining = same_line[
#                     alias_start + len(alias):
#                 ].strip()

#                 value = extract_value(
#                     remaining
#                 )

#                 if value is not None:

#                     print(
#                         f"FOUND SAME LINE: {remaining}"
#                     )

#             # ====================================================
#             # STRATEGY 2
#             # VALUE AFTER PARAMETER
#             # ====================================================

#             if value is None:

#                 end = min(
#                     i + 6,
#                     next_parameter_index
#                 )

#                 for j in range(
#                     i + 1,
#                     end
#                 ):

#                     candidate = lines[j]

#                     if j != i + 1:

#                         other_parameter = (
#                             find_parameter(candidate)
#                         )

#                         if other_parameter:

#                             break

#                     if is_unit(candidate):
#                         print(
#                             f"Skipping unit: {candidate}"
#                         )
#                         continue

#                     if is_method(candidate):
#                         print(
#                             f"Skipping method: {candidate}"
#                         )
#                         continue

#                     if is_reference_range(candidate):
#                         print(
#                             f"Skipping reference range: "
#                             f"{candidate}"
#                         )
#                         continue

#                     candidate_value = extract_value(
#                         candidate
#                     )

#                     if candidate_value is not None:

#                         value = candidate_value

#                         print(
#                             f"FOUND VALUE AFTER: "
#                             f"{candidate}"
#                         )

#                         break

#             # ====================================================
#             # STRATEGY 3
#             # VALUE BEFORE PARAMETER
#             # ====================================================

#             if value is None:

#                 start = max(
#                     previous_parameter_index + 1,
#                     i - 4
#                 )

#                 for j in range(
#                     i - 1,
#                     start - 1,
#                     -1
#                 ):

#                     candidate = lines[j]

#                     if is_unit(candidate):
#                         continue

#                     if is_method(candidate):
#                         continue

#                     if is_reference_range(candidate):
#                         continue

#                     candidate_value = extract_value(
#                         candidate
#                     )

#                     if candidate_value is not None:

#                         value = candidate_value

#                         print(
#                             f"FOUND VALUE BEFORE: "
#                             f"{candidate}"
#                         )

#                         break

#             # ====================================================
#             # SAVE
#             # ====================================================

#             if value is not None:

#                 parameters[parameter_id] = {
#                     "parameter_name": parameter_name,
#                     "parameter_id": parameter_id,
#                     "value": value,
#                     "matched_alias": alias
#                 }

#                 print(
#                     f"Saving: "
#                     f"{parameter_name} -> {value}"
#                 )

#             else:

#                 print(
#                     f"WARNING: Could not find value for "
#                     f"{parameter_name}"
#                 )

#         # ========================================================
#         # FINAL RESULT
#         # ========================================================

#         print(
#             "\n========== FINAL PARAMETERS =========="
#         )

#         for parameter_id, data in parameters.items():

#             print(
#                 f"{data['parameter_name']} "
#                 f"-> {data['value']} "
#                 f"(ID: {parameter_id})"
#             )

#         print(
#             f"\nTotal parameters extracted: "
#             f"{len(parameters)}"
#         )

#         return parameters
import json
import re

from app.models.parameter_alias import ParameterAlias
from app.providers.claude_provider import ClaudeProvider


class ReportParser:

    # ============================================================
    # MAIN REPORT PARSER
    # ============================================================

    @staticmethod
    def parse_report(text: str):

        if not text:
            return {
                "metadata": {},
                "parameters": {}
            }

        print("=" * 80)
        print("CLAUDE REPORT PARSER STARTED")
        print("=" * 80)

        # --------------------------------------------------------
        # Load all parameters from database
        # --------------------------------------------------------

        aliases = ParameterAlias.query.all()

        parameter_list = []

        seen_ids = set()

        for alias_obj in aliases:

            if not alias_obj.parameter:
                continue

            parameter = alias_obj.parameter

            if parameter.id in seen_ids:
                continue

            seen_ids.add(parameter.id)

            parameter_list.append({
                "id": parameter.id,
                "name": parameter.parameter_name,
                "unit": parameter.unit,
                "normal_min": parameter.normal_min,
                "normal_max": parameter.normal_max
            })

        print(
            f"Available master parameters: "
            f"{len(parameter_list)}"
        )

        # --------------------------------------------------------
        # Build Claude prompt
        # --------------------------------------------------------

        prompt = ReportParser.build_prompt(
            text,
            parameter_list
        )

        # --------------------------------------------------------
        # Call Claude
        # --------------------------------------------------------

        provider = ClaudeProvider()

        try:

            result = provider.generate_json(
                prompt
            )

        except Exception as e:

            print("=" * 80)
            print("CLAUDE PARSER ERROR")
            print(e)
            print("=" * 80)

            return {
                "metadata": {},
                "parameters": {}
            }

        # --------------------------------------------------------
        # Validate result
        # --------------------------------------------------------

        if not isinstance(result, dict):

            print(
                "Claude returned invalid JSON structure."
            )

            return {
                "metadata": {},
                "parameters": {}
            }

        metadata = result.get(
            "metadata",
            {}
        )

        claude_parameters = result.get(
            "parameters",
            []
        )

        # --------------------------------------------------------
        # Convert Claude parameter list
        # into existing application format
        #
        # Existing HealthReportService expects:
        #
        # {
        #     parameter_id: {
        #         parameter_name: "...",
        #         parameter_id: 1,
        #         value: 123
        #     }
        # }
        # --------------------------------------------------------

        parameters = {}

        for item in claude_parameters:

            try:

                parameter_id = int(
                    item.get("parameter_id")
                )

            except (
                TypeError,
                ValueError
            ):

                continue

            value = item.get(
                "value"
            )

            # ----------------------------------------------------
            # Ignore empty values
            # ----------------------------------------------------

            if value is None:
                continue

            # ----------------------------------------------------
            # Convert numeric strings
            # ----------------------------------------------------

            if isinstance(value, str):

                value = value.strip()

                if not value:
                    continue

                # Remove commas
                value = value.replace(
                    ",",
                    ""
                )

                try:

                    value = float(value)

                except ValueError:

                    # Qualitative results such as
                    # Positive / Negative / Absent
                    # are currently not saved because
                    # HealthParameter.value is numeric.

                    print(
                        f"Skipping non-numeric value: "
                        f"{value}"
                    )

                    continue

            # ----------------------------------------------------
            # Make sure value is numeric
            # ----------------------------------------------------

            if not isinstance(
                value,
                (int, float)
            ):

                continue

            parameters[parameter_id] = {

                "parameter_name": item.get(
                    "parameter_name"
                ),

                "parameter_id": parameter_id,

                "value": float(value),

                "matched_alias": item.get(
                    "matched_alias"
                ),

                "unit": item.get(
                    "unit"
                )
            }

        print("=" * 80)
        print("CLAUDE EXTRACTED PARAMETERS")
        print("=" * 80)

        for parameter_id, data in parameters.items():

            print(
                f"{data['parameter_name']} "
                f"-> {data['value']} "
                f"(ID: {parameter_id})"
            )

        print(
            f"Total parameters extracted: "
            f"{len(parameters)}"
        )

        print("=" * 80)

        return {
            "metadata": metadata,
            "parameters": parameters
        }

    # ============================================================
    # BUILD CLAUDE PROMPT
    # ============================================================

    @staticmethod
    def build_prompt(
        text,
        parameter_list
    ):

        parameter_json = json.dumps(
            parameter_list,
            indent=2
        )

        prompt = f"""
You are a medical laboratory report extraction engine.

Your job is to extract ONLY the actual laboratory test
results from the OCR text provided below.

The OCR may contain:
- patient information
- test names
- values
- units
- reference ranges
- methods
- comments
- doctor's names
- dates
- page numbers
- laboratory information
- explanations
- scientific references
- footnotes
- unrelated numbers

You MUST NOT treat arbitrary numbers in the report as test values.

============================================================
AVAILABLE PARAMETERS
============================================================

You may ONLY return parameters from this list.

{parameter_json}

============================================================
IMPORTANT EXTRACTION RULES
============================================================

1. Match a laboratory test to the closest parameter from
   the AVAILABLE PARAMETERS list.

2. Extract the ACTUAL RESULT VALUE belonging to that test.

3. NEVER use:
   - reference ranges
   - dates
   - page numbers
   - barcode numbers
   - lab codes
   - sample numbers
   - method numbers
   - scientific citation years
   - doctor's credentials
   - unrelated numbers
   - explanatory text

4. The value normally appears near the test name.

5. Example:

   FASTING BLOOD SUGAR(GLUCOSE)
   PHOTOMETRY
   104.19
   70-110

   Correct value:
   104.19

   Do NOT return:
   70
   110

6. Example:

   TOTAL CHOLESTEROL
   PHOTOMETRY
   153
   <200

   Correct value:
   153

7. If a test appears multiple times, choose the actual
   laboratory result corresponding to the test table.

8. Do NOT infer values from other tests.

9. Do NOT calculate missing values.

10. Do NOT copy numbers from explanatory paragraphs.

11. Do NOT match short aliases accidentally.

For example:
- "as" must NOT automatically mean Arsenic.
- "u" must NOT automatically mean Uranium.
- "mg" must NOT automatically mean Magnesium.
- "rbc" must only match when it clearly refers to RBC count.
- "u/l" must NOT be treated as Uranium.

12. The test name must have clear contextual evidence.

13. If you are not confident that a value belongs to a
    parameter, DO NOT return it.

14. Preserve the numeric value exactly as reported.

15. Do not use reference ranges to determine the value.

16. Do not extract values from the "Method", "Remarks",
    "Note", "Reference", or explanatory sections.

============================================================
QUALITATIVE RESULTS
============================================================

Some laboratory tests may have values such as:

Positive
Negative
Absent
Present
Nil
Trace
Normal

If the database value field only supports numeric values,
DO NOT return these qualitative parameters.

============================================================
PATIENT METADATA
============================================================

Extract if clearly available:

patient_name
age
gender
laboratory
referred_by
report_date

Do not guess missing metadata.

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Do NOT use markdown.

Use exactly this structure:

{{
    "metadata": {{
        "patient_name": null,
        "age": null,
        "gender": null,
        "laboratory": null,
        "referred_by": null,
        "report_date": null
    }},
    "parameters": [
        {{
            "parameter_id": 1,
            "parameter_name": "Hemoglobin",
            "value": 13.5,
            "unit": "g/dL",
            "matched_alias": "hemoglobin"
        }}
    ]
}}

Only include parameters where the actual laboratory
result value is clearly identifiable.

============================================================
OCR REPORT
============================================================

{text}
"""

        return prompt