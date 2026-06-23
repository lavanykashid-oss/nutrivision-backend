from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.meal import Meal
from app.config.database import db
from app.models.nutrition_analysis import NutritionAnalysis
from sqlalchemy import func

food_bp = Blueprint(
    "food",
    __name__
)


@food_bp.route("/analyze",methods=["POST"])
@jwt_required()
def analyze_food():

    

    image = request.files.get("image")

    food_name = request.form.get("food_name")
    user_id = get_jwt_identity()

    
    data = {
    "name": "Apple",
    "calories": 95,
    "protein": 0.5,
    "carbs": 25,
    "fat": 0.3,
    "fiber": 4.4,
    "sugar": 19,
    "sodium": 1,
    "vitamins": ["Vitamin C"],
    "healthScore": 90,
    "servingSize": "1 medium apple",
    "tags": ["Healthy"]
}


    meal = Meal(
    user_id=user_id,
    meal_name=food_name,
    meal_type="Snack"
)

    db.session.add(meal)
    db.session.commit()

    analysis = NutritionAnalysis(
    meal_id=meal.id,
    calories=data["calories"],
    protein=data["protein"],
    fat=data["fat"],
    carbs=data["carbs"],
    fiber=data["fiber"],
    sugar=data["sugar"],
    sodium=data["sodium"],
    vitamin_data=data["vitamins"],
    mineral_data=[]
)

    db.session.add(analysis)
    db.session.commit()

    print("Image:", image)
    print("Food Name:", food_name)
    print("meal id:", meal.id)

    

    return jsonify(data)

@food_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():

    user_id = get_jwt_identity()

    meals = Meal.query.filter_by(
        user_id=user_id
    ).all()

    history = []

    for meal in meals:

        analysis = NutritionAnalysis.query.filter_by(
            meal_id=meal.id
        ).first()

        if not analysis:
            continue

        history.append({
            "id": meal.id,
            "meal_name": meal.meal_name,
            "meal_type": meal.meal_type,
            "calories": analysis.calories if analysis else 0,
            "protein": analysis.protein if analysis else 0,
            "carbs": analysis.carbs if analysis else 0,
            "fat": analysis.fat if analysis else 0,

            "fiber": analysis.fiber if analysis else 0,
            "sugar": analysis.sugar if analysis else 0,
            "sodium": analysis.sodium if analysis else 0,

            "vitamins": analysis.vitamin_data if analysis else []

            
        })

    return jsonify(history)

@food_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    user_id = get_jwt_identity()

    meals = Meal.query.filter_by(
        user_id=user_id
    ).all()

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_fiber = 0
    total_sugar = 0
    total_sodium = 0

    health_scores = []

    recent_meals = []

    weekly_data = [
    {"day": "Mon", "calories": 0, "protein": 0},
    {"day": "Tue", "calories": 0, "protein": 0},
    {"day": "Wed", "calories": 0, "protein": 0},
    {"day": "Thu", "calories": 0, "protein": 0},
    {"day": "Fri", "calories": 0, "protein": 0},
    {"day": "Sat", "calories": 0, "protein": 0},
    {"day": "Sun", "calories": 0, "protein": 0},
]

    for meal in meals:

        analysis = NutritionAnalysis.query.filter_by(
            meal_id=meal.id
        ).first()

        if analysis:

            score = 100

            if analysis.calories and analysis.calories > 500:
                  score -= 10

            if analysis.sugar and analysis.sugar > 25:
                   score -= 10

            if analysis.fiber and analysis.fiber > 3:
              score += 5

            score = min(score,100)
            health_scores.append(score)


            

            total_calories += analysis.calories or 0
            total_protein += analysis.protein or 0
            total_carbs += analysis.carbs or 0
            total_fat += analysis.fat or 0
            total_fiber += analysis.fiber or 0
            total_sugar += analysis.sugar or 0
            total_sodium += analysis.sodium or 0

            day_index = meal.created_at.weekday()

            weekly_data[day_index]["calories"] += analysis.calories or 0
            weekly_data[day_index]["protein"] += analysis.protein or 0

            recent_meals.append({
                "meal_name": meal.meal_name,
                "calories": analysis.calories,
                "protein": analysis.protein
            })

    avg_health_score = (
        round(sum(health_scores) / len(health_scores))
        if health_scores
        else 0
)

   

    return jsonify({
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fat": total_fat,
        "total_fiber": total_fiber,
        "total_sugar": total_sugar,
        "total_sodium": total_sodium,

        "total_meals": len(meals),
        "recent_meals": recent_meals[-5:],
        "weekly_data": weekly_data,

        "health_score": avg_health_score

        
    })