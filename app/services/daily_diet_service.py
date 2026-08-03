from app.services.meal_planner_service import MealPlannerService
from app.models.meal_recipe import MealRecipe
class DailyDietService:

    @staticmethod
    def generate(report):

        meals = MealPlannerService.generate(report)

        analysis = report.analysis

        daily_plan = {

            "Breakfast": {
                "menu": [],
                "tips": ""
            },

            "Lunch": {
                "menu": [],
                "tips": ""
            },

            "Snack": {
                "menu": [],
                "tips": ""
            },

            "Dinner": {
                "menu": [],
                "tips": ""
            }

        }

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

              daily_plan[meal_name] = {

            "title": meal_template.title,

            "menu": meal_template.foods.split(","),

            "description": meal_template.description,

            "recommended_foods": meal["recommended_foods"],

            "benefits": meal["benefits"]

        }

        else:

         daily_plan[meal_name] = {

            "title": meal_name,

            "menu": meal["meal"].split(","),


            "description":meal["description"],

            "recommended_foods": meal["recommended_foods"],

            "benefits": meal["benefits"]

        }

            

        return daily_plan