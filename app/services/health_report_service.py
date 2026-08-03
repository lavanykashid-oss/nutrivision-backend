from app.config.database import db

from utils.ocr_service import OCRService
from utils.report_parser import ReportParser

from app.models.health_parameter import HealthParameter
from app.models.parameter_alias import ParameterAlias

from app.services.health_analysis_service import HealthAnalysisService

from app.repositories.health_report_repository import HealthReportRepository

from app.services.food_recommendation_service import FoodRecommendationService
class HealthReportService:

    @staticmethod
    def process_report(report):

        print(f"Processing Report {report.id}")

        # OCR
        text = OCRService.extract_text(report.file_path)

        print("="*80)
        print("OCR OUTPUT")
        print("="*80)
        print(text)
        print("="*80)



        report.ocr_text = text

        # Extract Parameters
        # extracted = ReportParser.parse_report(text)
        parsed = ReportParser.parse_report(text)

        metadata = parsed["metadata"]
        parameters = parsed["parameters"]

        # print(extracted)
        # print("TOTAL EXTRACTED:", len(extracted))
        # print(parsed)

        HealthParameter.query.filter_by(
            report_id=report.id
        ).delete()

        # Save Parameters


        for key, value in parameters.items():

            print("Searching alias for:", key)

            alias = ParameterAlias.query.filter(
                ParameterAlias.alias.ilike(key)
            ).first()

            if alias:
                print("FOUND:", alias.alias, "->", alias.parameter.parameter_name)
            else:
                print("NOT FOUND:", key)

            if not alias:
                print(f"Alias not found : {key}")
                continue

            master = alias.parameter

            flag = "Normal"

            if master.normal_min is not None and value < master.normal_min:
                flag = "Low"

            elif master.normal_max is not None and value > master.normal_max:
                flag = "High"

            print(f"Saving {master.parameter_name} = {value} ({flag})")

            parameters = HealthParameter(

                user_id=report.user_id,

                report_id=report.id,

                parameter_id=master.id,

                value=value,

                unit=master.unit,

                reference_low=master.normal_min,

                reference_high=master.normal_max,

                flag = flag

              
                

            )

            db.session.add(parameters)
        report.patient_name = metadata.get("patient_name")

        report.age = metadata.get("age")

        report.gender = metadata.get("gender")

        report.laboratory = metadata.get("laboratory")

        report.referred_by = metadata.get("referred_by")

        report.status = "processed"

        db.session.commit()
        HealthAnalysisService.analyze(report)

        FoodRecommendationService.get_recommendations(report.id)

        return True

    @staticmethod
    def get_report(report_id):

        return HealthReportRepository.get(report_id)

    
    @staticmethod
    def get_user_report(user_id):

        return HealthReportRepository.get_by_user(user_id)