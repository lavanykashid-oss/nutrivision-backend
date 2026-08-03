from app.services.diet_recommendation_service import DietRecommendationService


class DietPlanService:

    @staticmethod
    def generate(report):

        recommendations = DietRecommendationService.generate(report)

        meal_plan = {
            "Breakfast": [],
            "Lunch": [],
            "Dinner": [],
            "Snack": []
        }

        for item in recommendations:

            meal = item["meal_type"]

            if meal not in meal_plan:
                meal_plan[meal] = []

            meal_plan[meal].append({

                "food": item["food"],

                "parameter": item["parameter"],

                "reason": item["reason"]

            })

        return meal_plan