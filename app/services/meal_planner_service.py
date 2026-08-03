from app.services.diet_plan_service import DietPlanService
from app.models.meal_recipe import MealRecipe


class MealPlannerService:

    @staticmethod
    def generate(report):

        meals = DietPlanService.generate(report)

        analysis = report.analysis

        meal_plan = {}

        for meal_name, meal in meals.items():

            goal = None

            if analysis and analysis.deficiencies:

                deficiencies = analysis.deficiencies.split("\n")

                for item in deficiencies:

                    if "Hemoglobin" in item:
                        goal = "Iron Deficiency"

                    elif "Protein" in item:
                        goal = "High Protein"

                    elif "Packed Cell Volume" in item:
                        goal = "Hydration"

            meal_template = (
                MealRecipe.query
                .filter_by(
                    meal_type=meal_name,
                    goal=goal
                )
                .first()
            )

            if meal_template is None:

                meal_template = (
                    MealRecipe.query
                    .filter_by(
                        meal_type=meal_name
                    )
                    .first()
                )

            if meal_template:

                meal_plan[meal_name] = {

                    "title": meal_template.title,

                    "meal": meal_template.foods,

                    "description": meal_template.description,

                    "goal": meal_template.goal,

                    "recommended_foods": [
                        item["food"] for item in meal
                    ],

                    "benefits":list( 
                        {
                        item["reason"]
                        for item in meal
                        }
                    ),

                       

                }

            else:

                meal_plan[meal_name] = meal

        return meal_plan