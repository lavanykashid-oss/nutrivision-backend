import re

from app.models.parameter_alias import ParameterAlias


class ReportParser:


    @staticmethod
    def parse_report(text: str):


        metadata ={}

        # -------- Patient Name --------

        metadata["patient_name"] = None

        match = re.search(
    r"Patient\s*Name\s*[:\-]?\s*([^\n]+)",
    text,
    re.IGNORECASE
)

        if match:
            metadata["patient_name"] = match.group(1).strip()

        if metadata["patient_name"] is None:

            fallback = re.search(
        r"Dr\. Payal Shah[\s\S]*?\n([A-Za-z. ]+)\n\s*Age\s*:",
        text,
        re.IGNORECASE
    )

            if fallback:
               metadata["patient_name"] = fallback.group(1).strip()
#         patient = re.search(
#     r"Patient\s*Name[:\-]?\s*(.+)",
#     text,
#     re.IGNORECASE
# )

#         metadata["patient_name"] = (
#     patient.group(1).strip()
#     if patient else None
# )

# -------- Age --------
        age = re.search(
    r"Age\s*:\s*(\d+)\s*Years?",
    text,
    re.IGNORECASE
)

        metadata["age"] = (
    age.group(1).strip()
    if age else None
)

# -------- Gender --------
        gender = re.search(
    r"Sex\s*:\s*(Male|Female)",
    text,
    re.IGNORECASE
)

        metadata["gender"] = (
    gender.group(1).title()
    if gender else None
)

# -------- Laboratory --------
        lab = re.search(
    r"^(.*?)\n",
    text,
    re.MULTILINE
)

        metadata["laboratory"] = (
    lab.group(1).strip()
    if lab else None
)

# -------- Referred By --------
        doctor = re.search(
    r"Ref\.?\s*By\s*:\s*([^\n]+)",
    text,
    re.IGNORECASE
)

        metadata["referred_by"] = (
    doctor.group(1).strip()
    if doctor else None
)

#         doctor = re.search(
#     r"(?:Referred\s*By|Doctor|Consultant)[\s:]*([^\n]+)",
#     text,
#     re.IGNORECASE
# )

#         metadata["referred_by"] = (
#     doctor.group(1).strip()
#     if doctor else None
# )

        metadata["report_date"] = None

        match = re.search(
    r"(\d{2}[/-]\d{2}[/-]\d{4})",
    text
)

        if match:
               metadata["report_date"] = match.group(1)

        parameters = ReportParser.extract_parameters(text)

        return {
            "metadata": metadata,
            "parameters": parameters
}
    @staticmethod
    def extract_parameters(text):

     parameters = {}

    # -------------------------------
    # Load aliases from DB
    # -------------------------------
     aliases = ParameterAlias.query.all()

     alias_map = {}

     for a in aliases:
        alias_map[a.alias.lower().strip()] = a.parameter.parameter_name

    # Longest aliases first
     alias_items = sorted(
        alias_map.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )

    # -------------------------------
    # Normalize OCR lines
    # -------------------------------
     lines = []

     for line in text.splitlines():

        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    # -------------------------------
    # Ignore unwanted headings
    # -------------------------------
     ignore = {
        "spectrophotometry",
        "Spectrophotometry",
        "calculated",
        "Calculated",
        "High",
        "Low",
        "Reference",
        "high",
        "low",
        "normal",
        "reference value",
        "result",
        "unit",
        "investigation",
        "lipid profile",
        "blood indices",
        "differential wbc count"
        
    }

     print("\n========== PARSER START ==========\n")

    # -------------------------------
    # Process every OCR line
    # -------------------------------
     for i, line in enumerate(lines):

        lower_line = line.lower()

        if lower_line in ignore:
            continue

        matched_parameter = None
        matched_alias = None

        # -------------------------------
        # Find alias inside line
        # -------------------------------
        for alias, master_name in alias_items:

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, lower_line):

                matched_parameter = master_name
                matched_alias = alias
                break

        if matched_parameter is None:
            continue

        # Avoid duplicate extraction
        if matched_parameter in parameters:
            continue

        value = None

        # -------------------------------
        # Try extracting value
        # AFTER alias in same line
        # -------------------------------
        start = lower_line.find(matched_alias)

        remaining = line[start + len(matched_alias):]

        match = re.search(
            r"\d+(?:\.\d+)?",
            remaining
        )

        if match:
            value = float(match.group())

        # -------------------------------
        # Otherwise inspect next 3 lines
        # -------------------------------
        if value is None:

            for j in range(i + 1, min(i + 4, len(lines))):

                candidate = lines[j]

                candidate_lower = candidate.lower()

                # Stop if next parameter starts
                another_parameter = False

                for other_alias, _ in alias_items:

                    if other_alias in candidate_lower:
                        another_parameter = True
                        break

                if another_parameter:
                    break

                match = re.fullmatch(
                    r"\d+(?:\.\d+)?",
                    candidate
                )

                if match:

                    value = float(match.group())
                    break

        # -------------------------------
        # Save parameter
        # -------------------------------
        if value is not None:

            parameters[matched_parameter] = value

            print(
                f"{matched_parameter} -> {value}"
            )

     print("\n========== FINAL PARAMETERS ==========")
     print(parameters)

     return parameters
        

        








    # @staticmethod
    # def extract_parameters(text):

    #   parameters = {}

    # # -------------------------------
    # # Load all aliases from DB
    # # -------------------------------
    #   alias_map = {}

    #   aliases = ParameterAlias.query.all()

    #   for a in aliases:
    #     alias_map[a.alias.lower()] = a.parameter.parameter_name

    #     alias_items = sorted(
    #         alias_map.items(),
    #         key=lambda x: len(x[0]),
    #          reverse=True
    #     )

    # # -------------------------------
    # # Split OCR into lines
    # # -------------------------------
    # lines = []

    #    for line in text.splitlines():

    #         line = re.sub(r"\s+", " ", line)

    #         line = line.strip()

    #         if line:
    #            lines.append(line)

    #   parameter_order = []

    # # -------------------------------
    # # Find parameter names
    # # -------------------------------
    #   ignore = {
    #     "spectrophotometry",
    #     "calculated",
    #     "high",
    #     "low",
    #     "normal",
    #     "mg/dl",
    #     "%",
    #     "reference value",
    #     "result",
    #     "unit",
    #     "investigation",
    #     "lipid profile",
    # }

    #   for line in lines:

    #     clean = line.strip()

    #     if clean.lower() in ignore:
    #         continue

    #     matched_parameter = None

    #     for alias, master in alias_items:

    #         if alias in line.lower():

    #              matched_parameter = master

    #              break
    #         start = line.lower().find(alias)

    #         remaining = line[start + len(alias):]

    #         parameter_order.append(
    #             alias_map[clean.lower()]
    #         )

    # # -------------------------------
    # # Extract numeric values
    # # -------------------------------
    #   values = []

    #   for line in lines:

    #     m = re.fullmatch(
    #         r"\d+(?:\.\d+)?",
    #         remaining
    #     )

    #     if m:

    #         values = (
    #             float(m.group())
    #         )

    # for j in range(i+1, min(i+4, len(lines))):

    # candidate = lines[j]

    # if any(
    #     other_alias in candidate.lower()
    #     for other_alias, _ in alias_items
    # ):
    #     break

    # m = re.search(
    #     r"^\d+(?:\.\d+)?$",
    #     candidate
    # )

    # if m:

    #     value = float(m.group())

    #     break


    # # -------------------------------
    # # Pair parameters with values
    # # -------------------------------
    #   for name, value in zip(parameter_order, values):

    #     parameters[name] = value

    #   print("\nDetected Parameters")

    #   print(parameter_order)

    #   print("\nDetected Values")
    #   print(values)

    #   print("\nFinal Mapping")
    #   print(parameters)
 
    #   return parameters

    #     patterns = {

    #         "hemoglobin": r"Hemoglobin[\s\S]{0,80}?(\d+\.?\d*)",

    #         "rbc": r"Total\s+RBC\s+count[\s\S]{0,80}?(\d+\.?\d*)",

    #         "wbc": r"Total\s+WBC\s+count[\s\S]{0,80}?(\d+\.?\d*)",

    #         "pcv": r"Packed\s+Cell\s+Volume[\s\S]{0,80}?(\d+\.?\d*)",

    #         "mcv": r"Mean\s+Corpuscular\s+Volume[\s\S]{0,80}?(\d+\.?\d*)",

    #         "mch": r"\bMCH\b[\s\S]{0,60}?(\d+\.?\d*)",

    #         "mchc": r"\bMCHC\b[\s\S]{0,60}?(\d+\.?\d*)",

    #         "rdw": r"\bRDW\b[\s\S]{0,60}?(\d+\.?\d*)",

    #         "platelet": r"Platelet\s+Count[\s\S]{0,80}?(\d+\.?\d*)",

    #         "neutrophils": r"Neutrophils[\s\S]{0,40}?(\d+\.?\d*)",

    #         "lymphocytes": r"Lymphocytes[\s\S]{0,40}?(\d+\.?\d*)",

    #         "eosinophils": r"Eosinophils[\s\S]{0,40}?(\d+\.?\d*)",

    #         "monocytes": r"Monocytes[\s\S]{0,40}?(\d+\.?\d*)",

    #         "basophils": r"Basophils[\s\S]{0,40}?(\d+\.?\d*)",

    #     }

    #     for key, pattern in patterns.items():

    #         match = re.search(
    #             pattern,
    #             text,
    #             re.IGNORECASE | re.DOTALL
    #         )

    #         if match:

    #             value = match.group(1)

    #             try:
    #                 value = float(value)
    #             except ValueError:
    #                 continue

    #             parameters[key] = value

    #     return {
    #     "metadata": metadata,
    #     "parameters": parameters
    # }