# import sys
# import os

# sys.path.append(
#     os.path.dirname(
#         os.path.dirname(os.path.abspath(__file__))
#     )
# )
# from app import create_app
from app.config.database import db

from app.models.parameter_master import ParameterMaster
from app.models.parameter_alias import ParameterAlias


# app = create_app()


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

def seed_parameters():

    for item in CBC_PARAMETERS:

        existing = ParameterMaster.query.filter_by(
            parameter_name=item["name"]
        ).first()

        if not existing:

            parameter = ParameterMaster(
                parameter_name=item["name"],
                category=item["category"],
                unit=item["unit"],
                normal_min=item["min"],
                normal_max=item["max"]
            )

            db.session.add(parameter)
            db.session.flush()

        else:
            parameter = existing

        for alias in item["aliases"]:

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

    print("Parameter master seeded.")


# with app.app_context():

#     for item in CBC_PARAMETERS:

#         existing = ParameterMaster.query.filter_by(
#             parameter_name=item["name"]
#         ).first()

#         if existing:
#             print(f"Skipping {item['name']}")
#             continue

#         parameter = ParameterMaster(

#             parameter_name=item["name"],

#             category=item["category"],

#             unit=item["unit"],

#             normal_min=item["min"],

#             normal_max=item["max"]

#         )

#         db.session.add(parameter)
#         db.session.flush()

#         for alias in item["aliases"]:

#             db.session.add(

#                 ParameterAlias(

#                     parameter_id=parameter.id,

#                     alias=alias

#                 )

#             )

#     db.session.commit()

#     print("CBC Parameter Master Seeded Successfully.")