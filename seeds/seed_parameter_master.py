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

# import re
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
# ============================================================
# ADDITIONAL LIVER FUNCTION TEST PARAMETERS
# ============================================================

LFT_PARAMETERS = [

    {
        "name": "Bilirubin Direct",
        "category": "Liver Function Test",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Bilirubin Direct",
            "Direct Bilirubin",
            "Direct Bilirubin (DBIL)",
            "DBIL",
            "Conjugated Bilirubin"
        ]
    },

    {
        "name": "Albumin/Globulin Ratio",
        "category": "Liver Function Test",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Albumin/Globulin Ratio",
            "Albumin Globulin Ratio",
            "Albumin/Globulin",
            "A/G Ratio",
            "AG Ratio",
            "A:G Ratio"
        ]
    },

    {
        "name": "Bilirubin Total",
        "category": "Liver Function Test",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Bilirubin Total",
            "Total Bilirubin",
            "Total Bilirubin (TBIL)",
            "TBIL",
            "Serum Bilirubin Total"
        ]
    },

    {
        "name": "Globulin",
        "category": "Liver Function Test",
        "unit": "g/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Globulin",
            "Serum Globulin",
            "Calculated Globulin"
        ]
    },

    {
        "name": "SGOT/SGPT Ratio",
        "category": "Liver Function Test",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "SGOT/SGPT Ratio",
            "SGOT SGPT Ratio",
            "AST/ALT Ratio",
            "AST ALT Ratio"
        ]
    }
]


# ============================================================
# THYROID PROFILE PARAMETERS
# ============================================================
THYROID_PARAMETERS = [

    {
        "name": "Thyroxine (T4)",
        "category": "Thyroid Profile",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Thyroxine (T4)",
            "Thyroxine T4",
            "Total Thyroxine",
            "Total T4",
            "T4"
        ]
    },

    {
        "name": "Triiodothyronine (T3)",
        "category": "Thyroid Profile",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Triiodothyronine (T3)",
            "Triiodothyronine T3",
            "Total Triiodothyronine",
            "Total T3",
            "T3"
        ]
    },

    {
        "name": "Thyroid Stimulating Hormone - Ultrasensitive (UTSH)",
        "category": "Thyroid Profile",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Thyroid Stimulating Hormone - Ultrasensitive (UTSH)",
            "Thyroid Stimulating Hormone Ultrasensitive",
            "Ultrasensitive TSH",
            "TSH Ultrasensitive",
            "Thyroid Stimulating Hormone",
            "TSH",
            "UTSH"
        ]
    }
]


# ============================================================
# RENAL FUNCTION TEST PARAMETERS
# ============================================================

RENAL_PARAMETERS = [

    {
        "name": "Uric Acid",
        "category": "Renal Function Test",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Uric Acid",
            "Serum Uric Acid",
            "Uric Acid, Serum"
        ]
    },

    {
        "name": "Blood Urea Nitrogen (BUN)/Serum Urea",
        "category": "Renal Function Test",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Blood Urea Nitrogen (BUN)/Serum Urea",
            "Blood Urea Nitrogen (BUN)",
            "Blood Urea Nitrogen",
            "BUN",
            "Serum Urea",
            "Blood Urea"
        ]
    },

    {
        "name": "Calcium (Ca)",
        "category": "Renal Function Test",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Calcium (Ca)",
            "Calcium",
            "Serum Calcium",
            "Calcium Ca",
            "Ca"
        ]
    },

    {
        "name": "Creatinine",
        "category": "Renal Function Test",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Creatinine",
            "Serum Creatinine",
            "Creatinine, Serum"
        ]
    },

    {
        "name": "EGFR",
        "category": "Renal Function Test",
        "unit": "mL/min/1.73m²",
        "min": None,
        "max": None,
        "aliases": [
            "EGFR",
            "eGFR",
            "Estimated Glomerular Filtration Rate",
            "Estimated GFR",
            "GFR"
        ]
    },

    {
        "name": "BUN/Creatinine Ratio",
        "category": "Renal Function Test",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "BUN/Creatinine Ratio",
            "BUN Creatinine Ratio",
            "BUN/Creatinine",
            "BUN Creatinine"
        ]
    },

    {
        "name": "Urea/Creatinine Ratio",
        "category": "Renal Function Test",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Urea/Creatinine Ratio",
            "Urea Creatinine Ratio",
            "Urea/Creatinine"
        ]
    },

    {
        "name": "Urea (Calculated)",
        "category": "Renal Function Test",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Urea (Calculated)",
            "Calculated Urea",
            "Urea Calculated"
        ]
    }
]

# ============================================================
# URINE ROUTINE PARAMETERS
# ============================================================


URINE_PARAMETERS = [

    {
        "name": "Urine Protein",
        "category": "Urine routine",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Urine Protein",
            "Protein Urine",
            "Urinary Protein",
            "Protein, Urine"
        ]
    },

    {
        "name": "Specific Gravity",
        "category": "Urine routine",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Specific Gravity",
            "Urine Specific Gravity",
            "Specific Gravity of Urine",
            "SG"
        ]
    },

    {
        "name": "pH-value",
        "category": "Urine routine",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "pH-value",
            "pH Value",
            "Urine pH",
            "Urine PH",
            "pH"
        ]
    },

    {
        "name": "Nitrite",
        "category": "Urine routine",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Nitrite",
            "Nitrites",
            "Urine Nitrite",
            "Nitrite, Urine"
        ]
    },

    {
        "name": "Urine Glucose",
        "category": "Urine routine",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Urine Glucose",
            "Glucose Urine",
            "Urinary Glucose",
            "Glucose, Urine",
            "Urine Sugar"
        ]
    },

    {
        "name": "Ketones",
        "category": "Urine routine",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Ketones",
            "Urine Ketones",
            "Ketone Bodies",
            "Ketone Bodies, Urine",
            "Urinary Ketones"
        ]
    },

    {
        "name": "Urobilinogen",
        "category": "Urine routine",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Urobilinogen",
            "Urine Urobilinogen",
            "Urobilinogen, Urine"
        ]
    },

    {
        "name": "Urine Blood",
        "category": "Urine routine",
        "unit": "",
        "min": None,
        "max": None,
        "aliases": [
            "Urine Blood",
            "Blood Urine",
            "Blood in Urine",
            "Occult Blood",
            "Urine Occult Blood",
            "Blood, Urine"
        ]
    },
    {
    "name": "Epithelial Cells",
    "category": "Urine routine",
    "unit": "/HPF",
    "min": 0,
    "max": 5,
    "aliases": [
        "Epithelial Cells",
        "Epithelial cell",
        "Epithelial Cells / HPF",
        "Squamous Epithelial Cells",
        "Epithelial"
    ]
},

{
    "name": "Casts",
    "category": "Urine routine",
    "unit": "/LPF",
    "min": 0,
    "max": 0,
    "aliases": [
        "Casts",
        "Urinary Casts",
        "Hyaline Casts",
        "Casts / LPF"
    ]
},

{
    "name": "Urine Bilirubin",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Urine Bilirubin",
        "Bilirubin",
        "Urine Bile Pigment"
    ]
},

{
    "name": "Pus Cells",
    "category": "Urine routine",
    "unit": "/HPF",
    "min": 0,
    "max": 5,
    "aliases": [
        "Pus Cells",
        "Pus Cell",
        "Pus Cells / HPF",
        "WBC",
        "Urine WBC",
        "White Blood Cells"
    ]
},

{
    "name": "Crystals",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Crystals",
        "Urine Crystals",
        "Crystal"
    ]
},

{
    "name": "Colour",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Colour",
        "Color",
        "Urine Colour",
        "Urine Color"
    ]
},

{
    "name": "Appearance",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Appearance",
        "Urine Appearance",
        "Clarity",
        "Urine Clarity"
    ]
},

{
    "name": "Bile Pigment",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Bile Pigment",
        "Bile Pigments",
        "Urine Bile Pigment"
    ]
},

{
    "name": "Bacteria",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Bacteria",
        "Urine Bacteria",
        "Bacterial Cells"
    ]
},

{
    "name": "Bile Salt",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Bile Salt",
        "Bile Salts",
        "Urine Bile Salt"
    ]
},

{
    "name": "Red Blood Cells",
    "category": "Urine routine",
    "unit": "/HPF",
    "min": 0,
    "max": 3,
    "aliases": [
        "Red Blood Cells",
        "Red Blood Cell",
        "RBC",
        "Urine RBC",
        "RBC / HPF",
        "RBCs"
    ]
},

{
    "name": "MUCS",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "MUCS",
        "Mucus",
        "Mucus Threads",
        "Mucous Threads"
    ]
},

{
    "name": "Volume",
    "category": "Urine routine",
    "unit": "mL",
    "min": None,
    "max": None,
    "aliases": [
        "Volume",
        "Urine Volume",
        "Sample Volume"
    ]
},

{
    "name": "Yeast Cells",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Yeast Cells",
        "Yeast Cell",
        "Yeast",
        "Urine Yeast"
    ]
},

{
    "name": "Parasites",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Parasites",
        "Parasite",
        "Urine Parasites"
    ]
},

{
    "name": "Leukocyte Esterase",
    "category": "Urine routine",
    "unit": None,
    "min": None,
    "max": None,
    "aliases": [
        "Leukocyte Esterase",
        "Leucocyte Esterase",
        "Leukocyte esterase",
        "LE"
    ]
},

# =========================================================
# IRON PROFILE
# =========================================================

{
    "name": "Serum Iron",
    "category": "Iron Profile",
    "unit": "µg/dL",
    "min": 50,
    "max": 150,
    "aliases": [
        "Serum Iron",
        "Serum Fe",
        "Iron",
        "Iron, Serum",
        "Fe"
    ]
},

{
    "name": "Transferrin Saturation",
    "category": "Iron Profile",
    "unit": "%",
    "min": 20,
    "max": 50,
    "aliases": [
        "Transferrin Saturation",
        "Transferrin Saturation %",
        "Transferrin Sat",
        "Transferrin Saturation Ratio",
        "TSAT",
        "Iron Saturation",
        "Iron Saturation %"
    ]
},

{
    "name": "Total Iron Binding Capacity",
    "category": "Iron Profile",
    "unit": "µg/dL",
    "min": 250,
    "max": 400,
    "aliases": [
        "Total Iron Binding Capacity",
        "Total Iron-Binding Capacity",
        "TIBC",
        "Iron Binding Capacity",
        "Total Iron Binding Capacity (TIBC)"
    ]
},

{
    "name": "UIBC",
    "category": "Iron Profile",
    "unit": "µg/dL",
    "min": 111,
    "max": 343,
    "aliases": [
        "UIBC",
        "Unsaturated Iron Binding Capacity",
        "Unsaturated Iron-Binding Capacity",
        "Unsaturated Iron Binding Capacity (UIBC)",
        "Iron Unsaturated Binding Capacity"
    ]
},


]

ADVANCED_PARAMETERS = [

    # ============================================================
    # CARDIAC RISK MARKERS
    # ============================================================

    {
        "name": "High Sensitivity C-Reactive Protein (hs-CRP)",
        "category": "Cardiac Risk Markers",
        "unit": "mg/L",
        "min": None,
        "max": 3.0,
        "aliases": [
            "High Sensitivity C-Reactive Protein (hs-CRP)",
            "High Sensitivity CRP",
            "hs-CRP",
            "hsCRP",
            "High Sensitive CRP",
            "C-Reactive Protein High Sensitivity",
            "CRP High Sensitivity"
        ]
    },

    {
        "name": "Lipoprotein (A)",
        "category": "Cardiac Risk Markers",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Lipoprotein (A)",
            "Lipoprotein A",
            "Lp(a)",
            "LPA",
            "Lipoprotein-A"
        ]
    },

    {
        "name": "APO B/ APO A1 RATIO",
        "category": "Cardiac Risk Markers",
        "unit": "ratio",
        "min": None,
        "max": None,
        "aliases": [
            "APO B/ APO A1 RATIO",
            "Apo B/Apo A1 Ratio",
            "Apo B Apo A1 Ratio",
            "Apolipoprotein B/A1 Ratio",
            "Apo B:Apo A1",
            "ApoB/ApoA1 Ratio"
        ]
    },

    {
        "name": "Apolipoprotein A-1",
        "category": "Cardiac Risk Markers",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Apolipoprotein A-1",
            "Apolipoprotein A1",
            "Apo A-1",
            "Apo A1",
            "ApoA1",
            "Apolipoprotein A"
        ]
    },

    {
        "name": "Apolipoprotein B",
        "category": "Cardiac Risk Markers",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Apolipoprotein B",
            "Apo B",
            "ApoB",
            "Apolipoprotein B100",
            "Apo B100"
        ]
    },


    # ============================================================
    # DIABETIC SCREENING
    # ============================================================

    {
        "name": "Average Blood Glucose",
        "category": "Diabetic Screening",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Average Blood Glucose",
            "Average Blood Sugar",
            "Estimated Average Glucose",
            "Estimated Average Glucose (eAG)",
            "eAG",
            "Average Glucose"
        ]
    },

    {
        "name": "Blood Ketones",
        "category": "Diabetic Screening",
        "unit": "mmol/L",
        "min": None,
        "max": None,
        "aliases": [
            "Blood Ketones",
            "Blood Ketone",
            "Ketones",
            "Blood Beta Hydroxybutyrate",
            "Beta Hydroxybutyrate",
            "β-Hydroxybutyrate",
            "BHB"
        ]
    },

    {
        "name": "Fasting Blood Sugar (FBS)",
        "category": "Diabetic Screening",
        "unit": "mg/dL",
        "min": 70,
        "max": 99,
        "aliases": [
            "Fasting Blood Sugar (FBS)",
            "Fasting Blood Sugar",
            "FBS",
            "Fasting Blood Glucose",
            "Fasting Glucose",
            "Fasting Plasma Glucose",
            "FPG"
        ]
    },

    {
        "name": "Fructosamine",
        "category": "Diabetic Screening",
        "unit": "µmol/L",
        "min": 200,
        "max": 285,
        "aliases": [
            "Fructosamine",
            "Serum Fructosamine",
            "Fructosamine Serum"
        ]
    },

    {
        "name": "HbA1c (Glycosylated Hemoglobin)",
        "category": "Diabetic Screening",
        "unit": "%",
        "min": None,
        "max": None,
        "aliases": [
            "HbA1c (Glycosylated Hemoglobin)",
            "HbA1c",
            "Hb A1c",
            "Glycosylated Hemoglobin",
            "Glycated Hemoglobin",
            "Hemoglobin A1c",
            "A1c",
            "HBA1C"
        ]
    },

    {
        "name": "Insulin Fasting",
        "category": "Diabetic Screening",
        "unit": "µIU/mL",
        "min": None,
        "max": None,
        "aliases": [
            "Insulin Fasting",
            "Fasting Insulin",
            "Fasting Serum Insulin",
            "Insulin"
        ]
    },

    {
        "name": "Urine for microalbuminuria",
        "category": "Diabetic Screening",
        "unit": "mg/g creatinine",
        "min": None,
        "max": 30,
        "aliases": [
            "Urine for microalbuminuria",
            "Urine Microalbumin",
            "Microalbuminuria",
            "Urinary Microalbumin",
            "Urine Albumin",
            "Microalbumin",
            "MAU",
            "Urine ACR",
            "Albumin Creatinine Ratio"
        ]
    },


    # ============================================================
    # ELEMENTS - NUTRIENTS
    # ============================================================

    {
        "name": "Calcium - Nutrient",
        "category": "Elements",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Calcium - Nutrient",
            "Calcium",
            "Serum Calcium",
            "Ca"
        ]
    },

    {
        "name": "Magnesium - Nutrient",
        "category": "Elements",
        "unit": "mg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Magnesium - Nutrient",
            "Magnesium",
            "Serum Magnesium",
            "Mg"
        ]
    },

    {
        "name": "Iron - Nutrient",
        "category": "Elements",
        "unit": "µg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Iron - Nutrient",
            "Iron",
            "Serum Iron",
            "Fe"
        ]
    },

    {
        "name": "Copper - Nutrient",
        "category": "Elements",
        "unit": "µg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Copper - Nutrient",
            "Copper",
            "Serum Copper",
            "Cu"
        ]
    },

    {
        "name": "Zinc - Nutrient",
        "category": "Elements",
        "unit": "µg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Zinc - Nutrient",
            "Zinc",
            "Serum Zinc",
            "Zn"
        ]
    },

    {
        "name": "Selenium - Nutrient",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Selenium - Nutrient",
            "Selenium",
            "Serum Selenium",
            "Se"
        ]
    },

    {
        "name": "Manganese - Nutrient",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Manganese - Nutrient",
            "Manganese",
            "Serum Manganese",
            "Mn"
        ]
    },

    {
        "name": "Molybdenum - Nutrient",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Molybdenum - Nutrient",
            "Molybdenum",
            "Serum Molybdenum",
            "Mo"
        ]
    },

    {
        "name": "Chromium - Nutrient",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Chromium - Nutrient",
            "Chromium",
            "Serum Chromium",
            "Cr"
        ]
    },

    {
        "name": "Cobalt - Nutrient",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Cobalt - Nutrient",
            "Cobalt",
            "Serum Cobalt",
            "Co"
        ]
    },

    {
        "name": "Nickel - Nutrient",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Nickel - Nutrient",
            "Nickel",
            "Serum Nickel",
            "Ni"
        ]
    },


    # ============================================================
    # ELEMENTS - TOXIC
    # ============================================================

    {
        "name": "Arsenic - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Arsenic - Toxic",
            "Arsenic",
            "Blood Arsenic",
            "Urine Arsenic",
            "As"
        ]
    },

    {
        "name": "Cadmium - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Cadmium - Toxic",
            "Cadmium",
            "Blood Cadmium",
            "Urine Cadmium",
            "Cd"
        ]
    },

    {
        "name": "Mercury - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Mercury - Toxic",
            "Mercury",
            "Blood Mercury",
            "Urine Mercury",
            "Hg"
        ]
    },

    {
        "name": "Lead - Toxic",
        "category": "Elements",
        "unit": "µg/dL",
        "min": None,
        "max": None,
        "aliases": [
            "Lead - Toxic",
            "Lead",
            "Blood Lead",
            "Blood Lead Level",
            "Pb"
        ]
    },

    {
        "name": "Aluminium - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Aluminium - Toxic",
            "Aluminium",
            "Aluminum",
            "Blood Aluminium",
            "Aluminum",
            "Al"
        ]
    },

    {
        "name": "Barium - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Barium - Toxic",
            "Barium",
            "Ba"
        ]
    },

    {
        "name": "Thallium - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Thallium - Toxic",
            "Thallium",
            "Tl"
        ]
    },

    {
        "name": "Uranium - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Uranium - Toxic",
            "Uranium",
            "Urine Uranium",
            "U"
        ]
    },

    {
        "name": "Antimony - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Antimony - Toxic",
            "Antimony",
            "Sb"
        ]
    },

    {
        "name": "Tin - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Tin - Toxic",
            "Tin",
            "Sn"
        ]
    },

    {
        "name": "Silver - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Silver - Toxic",
            "Silver",
            "Ag"
        ]
    },

    {
        "name": "Vanadium - Toxic",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Vanadium - Toxic",
            "Vanadium",
            "V"
        ]
    },

    {
        "name": "Strontium",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Strontium",
            "Serum Strontium",
            "Sr"
        ]
    },

    {
        "name": "Caesium",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Caesium",
            "Cesium",
            "Cs"
        ]
    },

    {
        "name": "Beryllium",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Beryllium",
            "Be"
        ]
    },

    {
        "name": "Bismuth",
        "category": "Elements",
        "unit": "µg/L",
        "min": None,
        "max": None,
        "aliases": [
            "Bismuth",
            "Bi"
        ]
    }
]

def seed_parameters():

    all_parameters = CBC_PARAMETERS + OTHER_PARAMETERS + MORE_PARAMETERS + LFT_PARAMETERS + THYROID_PARAMETERS + RENAL_PARAMETERS + URINE_PARAMETERS + ADVANCED_PARAMETERS

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


