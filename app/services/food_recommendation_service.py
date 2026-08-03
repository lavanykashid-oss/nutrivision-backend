from app.models.health_report import HealthReport
from app.models.health_parameter import HealthParameter
from app.models.food_master import FoodMaster


class FoodRecommendationService:

    @staticmethod
    def get_recommendations(report_id):

        report = HealthReport.query.get(report_id)

        if not report:
            return []

        parameters = HealthParameter.query.filter(
            HealthParameter.report_id == report.id,
            HealthParameter.flag != "Normal"
        ).all()

        recommendations = []

        for p in parameters:

            print(
                p.parameter.parameter_name,
                p.flag
            )


            foods = FoodMaster.query.filter_by(
                parameter_id=p.parameter_id,
                condition=p.flag
            ).order_by(
                FoodMaster.priority
            ).all()


            for food in foods:
                recommendations.append({

                    "parameter": p.parameter.parameter_name,

                    "condition": p.flag,

                    "food": food.food_name,

                    "meal_type": food.meal_type,

                    "reason": food.reason


                })

        return recommendations