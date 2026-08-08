import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from app import create_app
from app.config.database import db

from app.models.parameter_master import ParameterMaster
from app.models.parameter_alias import ParameterAlias

import re
app = create_app()



CBC_PARAMETERS = [

    {
        "name": "Hemoglobin",
        "category": "CBC",
        "unit": "g/dL",
        "min": 13,
        "max": 17,
        "aliases": [
            "Hemoglobin",
            "Hemoglobin (Hb)",
            "Hb",
            "HB"
        ]
    },

    {
        "name": "RBC Count",
        "category": "CBC",
        "unit": "million/cumm",
        "min": 4.5,
        "max": 5.5,
        "aliases": [
            "RBC Count",
            "Total RBC count",
            "RBC"
        ]
    },

    {
        "name": "WBC Count",
        "category": "CBC",
        "unit": "cumm",
        "min": 4000,
        "max": 11000,
        "aliases": [
            "WBC Count",
            "Total WBC count",
            "WBC"
        ]
    },

    {
        "name": "Packed Cell Volume",
        "category": "CBC",
        "unit": "%",
        "min": 40,
        "max": 50,
        "aliases": [
            "Packed Cell Volume",
            "PCV",
            "Packed Cell Volume (PCV)"
        ]
    },

    {
        "name": "Mean Corpuscular Volume",
        "category": "CBC",
        "unit": "fL",
        "min": 83,
        "max": 101,
        "aliases": [
            "MCV",
            "Mean Corpuscular Volume",
            "Mean Corpuscular Volume (MCV)"
        ]
    },

    {
        "name": "MCH",
        "category": "CBC",
        "unit": "pg",
        "min": 27,
        "max": 32,
        "aliases": [
            "MCH"
        ]
    },

    {
        "name": "MCHC",
        "category": "CBC",
        "unit": "g/dL",
        "min": 32.5,
        "max": 34.5,
        "aliases": [
            "MCHC"
        ]
    },

    {
        "name": "RDW",
        "category": "CBC",
        "unit": "%",
        "min": 11.6,
        "max": 14,
        "aliases": [
            "RDW"
        ]
    },

    {
        "name": "Platelet Count",
        "category": "CBC",
        "unit": "cumm",
        "min": 150000,
        "max": 410000,
        "aliases": [
            "Platelet Count",
            "Platelets"
        ]
    },

    {
        "name": "Neutrophils",
        "category": "CBC",
        "unit": "%",
        "min": 50,
        "max": 62,
        "aliases": [
            "Neutrophils"
        ]
    },

    {
        "name": "Lymphocytes",
        "category": "CBC",
        "unit": "%",
        "min": 20,
        "max": 40,
        "aliases": [
            "Lymphocytes"
        ]
    },

    {
        "name": "Monocytes",
        "category": "CBC",
        "unit": "%",
        "min": 0,
        "max": 10,
        "aliases": [
            "Monocytes"
        ]
    },

    {
        "name": "Eosinophils",
        "category": "CBC",
        "unit": "%",
        "min": 0,
        "max": 6,
        "aliases": [
            "Eosinophils"
        ]
    },

    {
        "name": "Basophils",
        "category": "CBC",
        "unit": "%",
        "min": 0,
        "max": 2,
        "aliases": [
            "Basophils"
        ]
    }

]
OTHER_PARAMETERS = [

    {
        "name": "Amylase",
        "category": "General",
        "aliases": [
            "Amylase"
        ]
    },

    {
        "name": "Anti Cyclic Citrullinated Peptide Antibody (Anti CCP)",
        "category": "General",
        "aliases": [
            "Anti Cyclic Citrullinated Peptide Antibody (Anti CCP)",
            "Anti CCP",
            "Anti-CCP"
        ]
    },

    {
        "name": "Anti Nuclear Antibody / Factor (ANA / ANF)",
        "category": "General",
        "aliases": [
            "Anti Nuclear Antibody / Factor (ANA / ANF)",
            "ANA",
            "ANF"
        ]
    },

    {
        "name": "Chloride (Cl)",
        "category": "General",
        "aliases": [
            "Chloride (Cl)",
            "Chloride",
            "Cl"
        ]
    },

    {
        "name": "Ferritin",
        "category": "General",
        "aliases": [
            "Ferritin",
             "Ferritin Test",
             "Serum Ferritin"
        ]
    },

    {
        "name": "Homocysteine",
        "category": "General",
        "aliases": [
            "Homocysteine"
        ]
    },

    {
        "name": "Lipase",
        "category": "General",
        "aliases": [
            "Lipase"
        ]
    },

    {
        "name": "Magnesium",
        "category": "General",
        "aliases": [
            "Magnesium",
            "Mg"
        ]
    },

    {
        "name": "Serum Sodium (Na)",
        "category": "General",
        "aliases": [
            "Serum Sodium (Na)",
            "Sodium",
            "Na"
        ]
    },

    {
        "name": "Vitamin B12",
        "category": "General",
        "aliases": [
            "Vitamin B12",
            "Vit B12",
            "B12"
        ]
    },

    {
        "name": "Vitamin D Total",
        "category": "General",
        "aliases": [
            "Vitamin D Total",
            "Vitamin D",
            "Vit D"
        ]
    },

    {
        "name": "Serum Zinc",
        "category": "General",
        "aliases": [
            "Serum Zinc",
            "Zinc"
        ]
    }

]

MORE_PARAMETERS = [
    {
        "name": "LDL Cholestrol direct",
        "category": "Lipid Profile",
        "aliases": [
            "LDL Cholestrol direct",
            "Direct LDL",
            "LDL Direct",
            "LDL"
        ]
    },
    {
        "name": "Total Cholesterol",
        "category": "Lipid Profile",
        "aliases": [
            "Total Cholesterol",
            "Cholesterol",
            "TC"
        ]
    },
    {
        "name": "HDL Cholestrol",
        "category": "Lipid Profile",
        "aliases": [
            "HDL Cholestrol",
            "HDL",
            "HDL Cholesterol"
        ]
    },
    {
        "name": "Triglycerides",
        "category": "Lipid Profile",
        "aliases": [
            "Triglycerides",
            "TG",
            "Triglyceride"
        ]
    },
    {
        "name": "Serum VLDL cholestrol",
        "category": "Lipid Profile",
        "aliases": [
            "Serum VLDL cholestrol",
            "VLDL",
            "VLDL Cholesterol"
        ]
    },
    {
    "name": "Alkaline Phosphatase (ALP)",
    "category": "Liver Function Test",
    "aliases": [
        "Alkaline Phosphatase (ALP)",
        "Alkaline Phosphatase",
        "ALP"
    ]
},
{
    "name": "Alanine Transaminase (SGPT / ALT)",
    "category": "Liver Function Test",
    "aliases": [
        "Alanine Transaminase (SGPT / ALT)",
        "Alanine Transaminase",
        "SGPT",
        "ALT"
    ]
},
{
    "name": "Aspartate Aminotransferase (AST / SGOT)",
    "category": "Liver Function Test",
    "aliases": [
        "Aspartate Aminotransferase (AST / SGOT)",
        "Aspartate Aminotransferase",
        "AST",
        "SGOT"
    ]
},
{
    "name": "Serum Iron",
    "category": "Iron Profile",
    "aliases": [
        "Serum Iron",
        "Iron"
    ]
},
{
    "name": "Blood Urea Nitrogen (BUN)/Serum Urea",
    "category": "Renal Function Test",
    "aliases": [
        "Blood Urea Nitrogen (BUN)/Serum Urea",
        "Blood Urea Nitrogen",
        "BUN",
        "Serum Urea",
        "Urea"
    ]
},
{
    "name": "LDL/HDL ratio",
    "category": "Lipid Profile",
    "aliases": [
        "LDL/HDL ratio",
        "LDL HDL Ratio"
    ]
},
{
    "name": "Urea (Calculated)",
    "category": "Renal Function Test",
    "aliases": [
        "Urea (Calculated)",
        "Calculated Urea"
    ]
}


]

def seed_parameters():

    all_parameters = CBC_PARAMETERS + OTHER_PARAMETERS + MORE_PARAMETERS

    for item in all_parameters:

        existing = ParameterMaster.query.filter_by(
            parameter_name=item["name"]
        ).first()

        if not existing:

            parameter = ParameterMaster(
                parameter_name=item["name"],
                category=item["category"],
                unit=item.get("unit"),
                normal_min=item.get("min"),
                normal_max=item.get("max")
            )

            db.session.add(parameter)
            db.session.flush()

        else:
            parameter = existing

        for alias in item["aliases"]:

        # aliases = item.get("aliases")

        # if not aliases:
        #     aliases = generate_aliases(item["name"])

        # for alias in aliases:

            alias_exists = ParameterAlias.query.filter_by(
                alias=alias
            ).first()

            if not alias_exists:

                db.session.add(
                    ParameterAlias(
                        parameter_id=parameter.id,
                        alias=alias
                    )
                )

    db.session.commit()

    print("Parameter master seeded successfully.")


# import re


# def generate_aliases(parameter_name):

    # aliases = set()

    # aliases.add(parameter_name)

    # # Remove text inside brackets
    # no_brackets = re.sub(r"\s*\(.*?\)", "", parameter_name).strip()

    # aliases.add(no_brackets)

    # # Extract abbreviation inside brackets
    # match = re.search(r"\((.*?)\)", parameter_name)

    # if match:

    #     short = match.group(1).strip()

    #     aliases.add(short)

    # # Remove "Serum"
    # if no_brackets.lower().startswith("serum "):

    #     aliases.add(no_brackets.replace("Serum ", ""))

    # # Remove "Total"
    # aliases.add(no_brackets.replace("Total ", ""))

    # # Remove multiple spaces
    # aliases = {a.strip() for a in aliases if a.strip()}

    # return list(aliases)

# def seed_parameters():

#     for item in CBC_PARAMETERS:

#         existing = ParameterMaster.query.filter_by(
#             parameter_name=item["name"]
#         ).first()

#         if not existing:

#             parameter = ParameterMaster(
#                 parameter_name=item["name"],
#                 category=item["category"],
#                 unit=item["unit"],
#                 normal_min=item["min"],
#                 normal_max=item["max"]
#             )

#             db.session.add(parameter)
#             db.session.flush()

#         else:
#             parameter = existing

#         for alias in item["aliases"]:

#             alias_exists = ParameterAlias.query.filter_by(
#                 alias=alias
#             ).first()

#             if not alias_exists:

#                 db.session.add(
#                     ParameterAlias(
#                         parameter_id=parameter.id,
#                         alias=alias
#                     )
#                 )

#     db.session.commit()

#     print("Parameter master seeded.")


