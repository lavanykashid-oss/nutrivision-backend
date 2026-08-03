import re


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

        

        parameters = {}

        patterns = {

            "hemoglobin": r"Hemoglobin[\s\S]{0,80}?(\d+\.?\d*)",

            "rbc": r"Total\s+RBC\s+count[\s\S]{0,80}?(\d+\.?\d*)",

            "wbc": r"Total\s+WBC\s+count[\s\S]{0,80}?(\d+\.?\d*)",

            "pcv": r"Packed\s+Cell\s+Volume[\s\S]{0,80}?(\d+\.?\d*)",

            "mcv": r"Mean\s+Corpuscular\s+Volume[\s\S]{0,80}?(\d+\.?\d*)",

            "mch": r"\bMCH\b[\s\S]{0,60}?(\d+\.?\d*)",

            "mchc": r"\bMCHC\b[\s\S]{0,60}?(\d+\.?\d*)",

            "rdw": r"\bRDW\b[\s\S]{0,60}?(\d+\.?\d*)",

            "platelet": r"Platelet\s+Count[\s\S]{0,80}?(\d+\.?\d*)",

            "neutrophils": r"Neutrophils[\s\S]{0,40}?(\d+\.?\d*)",

            "lymphocytes": r"Lymphocytes[\s\S]{0,40}?(\d+\.?\d*)",

            "eosinophils": r"Eosinophils[\s\S]{0,40}?(\d+\.?\d*)",

            "monocytes": r"Monocytes[\s\S]{0,40}?(\d+\.?\d*)",

            "basophils": r"Basophils[\s\S]{0,40}?(\d+\.?\d*)",

        }

        for key, pattern in patterns.items():

            match = re.search(
                pattern,
                text,
                re.IGNORECASE | re.DOTALL
            )

            if match:

                value = match.group(1)

                try:
                    value = float(value)
                except ValueError:
                    continue

                parameters[key] = value

        return {
        "metadata": metadata,
        "parameters": parameters
    }