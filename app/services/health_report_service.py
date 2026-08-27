# from app.config.database import db

# from utils.ocr_service import OCRService
# from utils.report_parser import ReportParser

# from app.models.health_parameter import HealthParameter
# from app.models.parameter_alias import ParameterAlias

# from app.services.health_analysis_service import HealthAnalysisService

# from app.repositories.health_report_repository import HealthReportRepository

# from app.services.food_recommendation_service import FoodRecommendationService
# class HealthReportService:

#     @staticmethod
#     def process_report(report):

#         print(f"Processing Report {report.id}")

#         # OCR
#         text = OCRService.extract_text(report.file_path)

#         print("="*80)
#         print("OCR OUTPUT")
#         print("="*80)
#         print(text)
#         print("="*80)



#         report.ocr_text = text

#         # Extract Parameters
#         # extracted = ReportParser.parse_report(text)
#         parsed = ReportParser.parse_report(text)

#         metadata = parsed["metadata"]
#         parameters = parsed["parameters"]

#         # print(extracted)
#         # print("TOTAL EXTRACTED:", len(extracted))
#         # print(parsed)

#         HealthParameter.query.filter_by(
#             report_id=report.id
#         ).delete()

#         # Save Parameters


#         for key, value in parameters.items():

#             print("Searching alias for:", key)

#             alias = ParameterAlias.query.filter(
#                 ParameterAlias.alias.ilike(key)
#             ).first()

#             if alias:
#                 print("FOUND:", alias.alias, "->", alias.parameter.parameter_name)
#             else:
#                 print("NOT FOUND:", key)

#             if not alias:
#                 print(f"Alias not found : {key}")
#                 continue

#             master = alias.parameter

#             flag = "Normal"

#             if master.normal_min is not None and value < master.normal_min:
#                 flag = "Low"

#             elif master.normal_max is not None and value > master.normal_max:
#                 flag = "High"

#             print(f"Saving {master.parameter_name} = {value} ({flag})")

#             parameters = HealthParameter(

#                 user_id=report.user_id,

#                 report_id=report.id,

#                 parameter_id=master.id,

#                 value=value,

#                 unit=master.unit,

#                 reference_low=master.normal_min,

#                 reference_high=master.normal_max,

#                 flag = flag

              
                

#             )

#             db.session.add(parameters)
#         report.patient_name = metadata.get("patient_name")

#         report.age = metadata.get("age")

#         report.gender = metadata.get("gender")

#         report.laboratory = metadata.get("laboratory")

#         report.referred_by = metadata.get("referred_by")

#         report.status = "processed"

#         db.session.commit()
#         HealthAnalysisService.analyze(report)

#         FoodRecommendationService.get_recommendations(report.id)

#         return True

#     @staticmethod
#     def get_report(report_id):

#         return HealthReportRepository.get(report_id)

    
#     @staticmethod
#     def get_user_report(user_id):

#         return HealthReportRepository.get_by_user(user_id)

from app.config.database import db

from utils.ocr_service import OCRService
from utils.report_parser import ReportParser
# from utils.claude_report_parser import ClaudeReportParser
from app.models.health_parameter import HealthParameter
from app.models.parameter_master import ParameterMaster

from app.services.health_analysis_service import HealthAnalysisService

from app.repositories.health_report_repository import HealthReportRepository

from app.services.food_recommendation_service import FoodRecommendationService


class HealthReportService:

    @staticmethod
    def process_report(report):

        print(f"Processing Report {report.id}")

        # ========================================================
        # OCR
        # ========================================================

        text = OCRService.extract_text(
            report.file_path
        )

        print("=" * 80)
        print("OCR OUTPUT")
        print("=" * 80)
        print(text)
        print("=" * 80)

        report.ocr_text = text

        # ========================================================
        # PARSE REPORT
        # ========================================================

        parsed = ReportParser.parse_report(text)

        metadata = parsed["metadata"]
        extracted_parameters = parsed["parameters"]

        print("=" * 80)
        print("EXTRACTED PARAMETERS")
        print("=" * 80)

        for parameter_id, data in extracted_parameters.items():

            print(
                f"{data['parameter_name']} "
                f"= {data['value']} "
                f"(ID: {parameter_id})"
            )

        print("=" * 80)

        # ========================================================
        # DELETE OLD PARAMETERS
        # ========================================================

        HealthParameter.query.filter_by(
            report_id=report.id
        ).delete(
            synchronize_session=False
        )

        # ========================================================
        # SAVE PARAMETERS
        # ========================================================

        saved_count = 0

        for parameter_id, data in extracted_parameters.items():

            value = data["value"]

            parameter_name = data["parameter_name"]

            print(
                f"\nSaving parameter:"
            )

            print(
                f"Name      : {parameter_name}"
            )

            print(
                f"Parameter ID: {parameter_id}"
            )

            print(
                f"Value     : {value}"
            )

            # ----------------------------------------------------
            # Get master parameter directly
            # ----------------------------------------------------

            master = ParameterMaster.query.get(
                parameter_id
            )

            if not master:

                print(
                    f"ERROR: ParameterMaster not found "
                    f"for ID {parameter_id}"
                )

                continue

            # ----------------------------------------------------
            # Determine flag
            # ----------------------------------------------------

            # flag = "Normal"

            # if (
            #     master.normal_min is not None
            #     and value < master.normal_min
            # ):

            #     flag = "Low"

            # elif (
            #     master.normal_max is not None
            #     and value > master.normal_max
            # ):

            #     flag = "High"

            # ----------------------------------------------------
            # Create HealthParameter
            # ----------------------------------------------------

            raw_value = data.get("value")

            numeric_value = None
            raw_text_value = None

            if isinstance(raw_value, (int, float)):
                numeric_value = float(raw_value)

            elif isinstance(raw_value, str):
                cleaned = raw_value.strip()

                try:
                    numeric_value = float(cleaned.replace(",",""))

                except ValueError:
                    raw_text_value = cleaned

            flag = "Normal"

            if numeric_value is not None:

                if (
                    master.normal_min is not None 
                    and numeric_value < master.normal_min
                ):
                    flag = "Low"

                elif (
                    master.normal_max is not None 
                    and numeric_value > master.normal_max

                ):
                    flag = "High"

            health_parameter = HealthParameter(

                user_id=report.user_id,

                report_id=report.id,

                parameter_id=master.id,

                value=numeric_value,

                raw_text = raw_text_value,

                unit=data.get("unit"),

                reference_low=master.normal_min,

                reference_high=master.normal_max,

                flag=flag
            )

            db.session.add(
                health_parameter
            )

            saved_count += 1

            print(
                f"SAVED: "
                f"{master.parameter_name} "
                f"= {value} "
                f"({flag})"
            )

        # ========================================================
        # REPORT METADATA
        # ========================================================

        report.patient_name = metadata.get(
            "patient_name"
        )

        report.age = metadata.get(
            "age"
        )

        report.gender = metadata.get(
            "gender"
        )

        report.laboratory = metadata.get(
            "laboratory"
        )

        report.referred_by = metadata.get(
            "referred_by"
        )

        # ========================================================
        # STATUS
        # ========================================================

        if saved_count > 0:

            report.status = "processed"

        else:
            report.status = "failed"

        # ========================================================
        # COMMIT
        # ========================================================

        try:

            db.session.commit()

            print("=" * 80)
            print(
                f"SUCCESS: {saved_count} parameters "
                f"saved to database."
            )
            print("=" * 80)

        except Exception as e:

            db.session.rollback()

            print("=" * 80)
            print(
                "DATABASE ERROR:"
            )
            print(e)
            print("=" * 80)

            raise

        # ========================================================
        # AI ANALYSIS
        # ========================================================

        try:

            HealthAnalysisService.analyze(
                report
            )

        except Exception as e:

            print(
                "Health analysis failed:"
            )

            print(e)

        # ========================================================
        # FOOD RECOMMENDATION
        # ========================================================

        try:

            FoodRecommendationService.get_recommendations(
                report.id
            )

        except Exception as e:

            print(
                "Food recommendation failed:"
            )

            print(e)

        return True

    # ============================================================
    # GET REPORT
    # ============================================================

    @staticmethod
    def get_report(report_id):

        return HealthReportRepository.get(
            report_id
        )

    # ============================================================
    # GET USER REPORTS
    # ============================================================

    @staticmethod
    def get_user_report(user_id):

        return HealthReportRepository.get_by_user(
            user_id
        )