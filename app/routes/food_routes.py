from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.meal import Meal
from app.config.database import db
from app.models.nutrition_analysis import NutritionAnalysis

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