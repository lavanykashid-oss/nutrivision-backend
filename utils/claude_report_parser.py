from app.models.parameter_master import ParameterMaster
from app.providers.claude_provider import ClaudeProvider


class ClaudeReportParser:

    @staticmethod
    def parse_report(text):

        print("=" * 80)
        print("CLAUDE REPORT PARSER STARTED")
        print("=" * 80)

        # ========================================================
        # LOAD MASTER PARAMETERS
        # ========================================================

        masters = ParameterMaster.query.all()

        master_parameters = []

        for parameter in masters:

            master_parameters.append({

                "id": parameter.id,

                "name": parameter.parameter_name,

                "unit": parameter.unit,

                "normal_min": parameter.normal_min,

                "normal_max": parameter.normal_max
            })

        print(
            "Available master parameters:",
            len(master_parameters)
        )

        # ========================================================
        # PROMPT
        # ========================================================

        prompt = f"""
You are a medical laboratory report extraction engine.

Your job is ONLY to extract laboratory test results from the
provided OCR text.

DO NOT diagnose the patient.
DO NOT interpret the medical condition.
DO NOT invent values.

The OCR text may contain:

- multiple pages
- repeated patient information
- reference ranges
- units
- methods
- calculated values
- explanatory paragraphs
- tables converted into lines
- OCR errors

You must identify actual TEST NAME + RESULT VALUE pairs.

IMPORTANT:

The value must belong to the test immediately associated with it.

Example:

TOTAL CHOLESTEROL
PHOTOMETRY
< 200
mg/dl
153

Correct result:

Total Cholesterol = 153

NOT:

Total Cholesterol = 200


Another example:

ALKALINE PHOSPHATASE
PHOTOMETRY
45 - 129
U/L
107.4

Correct:

Alkaline Phosphatase = 107.4


Do NOT use:

- reference ranges
- units
- dates
- page numbers
- barcode numbers
- lab codes
- phone numbers
- doctor names
- addresses
- method numbers
- scientific citations

as laboratory result values.

============================================================
AVAILABLE MASTER PARAMETERS
============================================================

{master_parameters}

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

No Markdown.

No explanation.

No ```json.

Use exactly this structure:

{{
    "metadata": {{
        "patient_name": null,
        "age": null,
        "gender": null,
        "laboratory": null,
        "referred_by": null
    }},

    "parameters": [
        {{
            "parameter_id": 1,
            "parameter_name": "Hemoglobin",
            "value": 17,
            "unit": "g/dL"
        }}
    ]
}}

============================================================
PARAMETER MATCHING
============================================================

You MUST match every extracted test to the closest parameter
from AVAILABLE MASTER PARAMETERS.

Use parameter_id from the master list.

Do not create a new parameter.

If a test is not confidently matched to a master parameter,
do not include it.

============================================================
QUALITATIVE RESULTS
============================================================

Some tests contain text values such as:

ABSENT
PRESENT
NEGATIVE
POSITIVE
CLEAR
PALE YELLOW
NIL

These are valid laboratory results.

For qualitative values, use:

"value": "ABSENT"

Do not convert qualitative results to numbers.

============================================================
NUMERIC RESULTS
============================================================

Preserve the actual reported value.

Examples:

153
42
0.45
259
107.4
184
229.3
0.68
126
4.9

Do not use the reference range.

============================================================
IMPORTANT
============================================================

The report contains multiple pages.

Extract ALL valid laboratory parameters.

Do not stop after the first page.

Do not return duplicate parameters.

If the same parameter appears more than once,
use the actual laboratory result associated with the
test table, not a value appearing in explanatory text.

OCR TEXT:

{text}
"""

        # ========================================================
        # CALL CLAUDE
        # ========================================================

        provider = ClaudeProvider()

        result = provider.generate_json(
            prompt
        )

        # ========================================================
        # FAILURE
        # ========================================================

        if not result:

            print("=" * 80)
            print("CLAUDE PARSER RETURNED NO DATA")
            print("=" * 80)

            return {
                "metadata": {},
                "parameters": {}
            }

        # ========================================================
        # CONVERT PARAMETERS TO DICT
        # ========================================================

        extracted = {}

        for item in result.get(
            "parameters",
            []
        ):

            parameter_id = item.get(
                "parameter_id"
            )

            value = item.get(
                "value"
            )

            if parameter_id is None:
                continue

            if value is None:
                continue

            extracted[
                parameter_id
            ] = {

                "parameter_id":
                    parameter_id,

                "parameter_name":
                    item.get(
                        "parameter_name"
                    ),

                "value":
                    value,

                "unit":
                    item.get(
                        "unit"
                    )
            }

        print("=" * 80)
        print(
            "CLAUDE PARAMETERS EXTRACTED:",
            len(extracted)
        )
        print("=" * 80)

        for parameter_id, data in extracted.items():

            print(
                data["parameter_name"],
                "=",
                data["value"],
                "(ID:",
                parameter_id,
                ")"
            )

        return {

            "metadata":
                result.get(
                    "metadata",
                    {}
                ),

            "parameters":
                extracted
        }