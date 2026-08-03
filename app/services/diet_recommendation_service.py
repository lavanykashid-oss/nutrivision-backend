from app.models.health_analysis import HealthAnalysis
from app.models.food_master import FoodMaster


class DietRecommendationService:

    @staticmethod
    def generate(report):

        analysis = report.analysis

        if not analysis:
            return []

        recommendations = []

        deficiencies = analysis.deficiencies.split("\n")

        for item in deficiencies:

            if " is " not in item:
                continue

            parameter_name, condition = item.split(" is ")

            foods = (
                FoodMaster.query
                .join(FoodMaster.parameter)
                .filter_by(
                    parameter_name=parameter_name
                )
                .filter(
                    FoodMaster.condition == condition
                )
                .order_by(FoodMaster.priority)
                .all()
            )

            for food in foods:

                recommendations.append({
                    "parameter": parameter_name,
                    "condition": condition,
                    "food": food.food_name,
                    "meal_type": food.meal_type,
                    "reason": food.reason
                })

        return recommendations