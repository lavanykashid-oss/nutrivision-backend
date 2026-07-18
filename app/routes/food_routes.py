from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.meal import Meal
from app.config.database import db
from app.models.nutrition_analysis import NutritionAnalysis

from PIL import Image
from app.services.ai_service import AIService
import imagehash

from datetime import datetime, timedelta

import cloudinary.uploader
from app.config.cloudinary_config import *

import os
import uuid
from werkzeug.utils import secure_filename


from app.utils.image_hash import generate_image_hash
from app.utils.perceptual_hash import generate_phash




food_bp = Blueprint(
    "food",
    __name__
)
def save_cached_analysis(user_id, cached, image_hash, perceptual_hash):

    meal = Meal(
        user_id=user_id,
        meal_name=cached.meal.meal_name,
        meal_type=cached.meal_type_ai,
        image_url=cached.meal.image_url
    )

    db.session.add(meal)
    db.session.commit()

    analysis = NutritionAnalysis(
        meal_id=meal.id,

        image_hash=image_hash,
        perceptual_hash=perceptual_hash,

        calories=cached.calories,
        protein=cached.protein,
        carbs=cached.carbs,
        fat=cached.fat,
        fiber=cached.fiber,
        sugar=cached.sugar,
        sodium=cached.sodium,

        vitamin_data=cached.vitamin_data,
        mineral_data=cached.mineral_data,

        confidence=cached.confidence,
        meal_type_ai=cached.meal_type_ai,
        serving_size=cached.serving_size,
        health_score=cached.health_score,
        health_tips=cached.health_tips,
        warnings=cached.warnings,
        tags=cached.tags
    )

    db.session.add(analysis)
    db.session.commit()

    return jsonify({
        "name": meal.meal_name,
        "confidence": analysis.confidence,
        "mealType": analysis.meal_type_ai,
        "servingSize": analysis.serving_size,

        "calories": analysis.calories,
        "protein": analysis.protein,
        "carbs": analysis.carbs,
        "fat": analysis.fat,
        "fiber": analysis.fiber,
        "sugar": analysis.sugar,
        "sodium": analysis.sodium,

        "vitamins": analysis.vitamin_data,
        "minerals": analysis.mineral_data,

        "healthScore": analysis.health_score,
        "healthTips": analysis.health_tips,
        "warnings": analysis.warnings,
        "tags": analysis.tags,

        "cached": True
    })


@food_bp.route("/analyze", methods=["POST"])
@jwt_required()
def analyze_food():

    image_hash = None
    perceptual_hash = None

    food_name = request.form.get("food_name")
    description = request.form.get("description", "")
   

    image = request.files.get("image")
    food_name = request.form.get("food_name")
    image_path = None

    user_id = get_jwt_identity()

    if not image and not food_name:
        return jsonify({
            "message": "Please upload an image or enter a food name."
        }), 400

    # --------------------------------------------------
    # Exact Image Cache
    # --------------------------------------------------

    if image:

        # upload_folder = os.path.join("uploads", "meals")
        # os.makedirs(upload_folder, exist_ok=True)

        # extension = os.path.splitext(image.filename)[1]

        # filename = f"{uuid.uuid4()}{extension}"

        # filepath = os.path.join(upload_folder, filename)

        # image.save(filepath)

        # image.seek(0)

        # image_path = f"uploads/meals/{filename}"
        result = cloudinary.uploader.upload(
          image,
          folder="nutrivision/meals"
)

        image_path = result["secure_url"]

        image.seek(0)


        image_hash = generate_image_hash(image)
        perceptual_hash = generate_phash(image)

        cached = NutritionAnalysis.query.filter_by(
            image_hash=image_hash
        ).first()

        if cached:
            return save_cached_analysis(
                user_id,
                cached,
                image_hash,
                perceptual_hash
            )

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    prompt = f"""
You are NutriVision AI.

If an image is provided, analyze the image.

If only a food name is provided, estimate nutrition using the food name.

Food:
{food_name}

Additional Description
{description}

Return ONLY valid JSON.

Schema:

{{
  "name": "",
  "confidence": 0,
  "mealType": "",
  "servingSize": "",

  "calories": 0,
  "protein": 0,
  "carbs": 0,
  "fat": 0,
  "fiber": 0,
  "sugar": 0,
  "sodium": 0,

  "vitamins": [],
  "minerals": [],

  "healthScore": 0,

  "healthTips": [],

  "warnings": [],

  "tags": []
}}

Requirements:

- confidence: integer (0-100)
- healthScore: integer (0-100)
- mealType: Breakfast, Lunch, Dinner, Snack or Drink
- healthTips: exactly 2 (maximum 4 words each)
- warnings: maximum 2
- vitamins: maximum 2
- minerals: maximum 2
- tags: maximum 3

Estimate nutrition realistically.

If no food is detected return:

{{
    "error":"NO_FOOD_DETECTED"
}}
"""

    # --------------------------------------------------
    # Similar Image Cache
    # --------------------------------------------------

    if image:

        current_hash = imagehash.hex_to_hash(perceptual_hash)

        all_hashes = NutritionAnalysis.query.all()

        cached = None

        for item in all_hashes:

            if not item.perceptual_hash:
                continue

            db_hash = imagehash.hex_to_hash(item.perceptual_hash)

            distance = current_hash - db_hash

            if distance <= 5:
                cached = item
                break

        if cached:
            return save_cached_analysis(
                user_id,
                cached,
                image_hash,
                perceptual_hash
            )

    # --------------------------------------------------
    # AI Request
    # --------------------------------------------------

    try:

        if image:

            data = AIService.generate_json(
                prompt=prompt,
                image=image
            )

        else:

            data = AIService.generate_json(
                prompt=prompt
            )

    except Exception as e:

        print(e)

        return jsonify({
            "message": "AI analysis failed"
        }), 500

    # --------------------------------------------------
    # Save Meal
    # --------------------------------------------------

    meal = Meal(
        user_id=user_id,
        meal_name=data.get("name") or food_name or "Unknown Food",
        meal_type=data.get("mealType", "Snack"),
        image_url=image_path
    )

    db.session.add(meal)
    db.session.commit()

    # --------------------------------------------------
    # Save Analysis
    # --------------------------------------------------

    analysis = NutritionAnalysis(

        meal_id=meal.id,

        image_hash=image_hash,
        perceptual_hash=perceptual_hash,

        calories=data.get("calories", 0),
        protein=data.get("protein", 0),
        carbs=data.get("carbs", 0),
        fat=data.get("fat", 0),
        fiber=data.get("fiber", 0),
        sugar=data.get("sugar", 0),
        sodium=data.get("sodium", 0),

        vitamin_data=data.get("vitamins", []),
        mineral_data=data.get("minerals", []),

        confidence=data.get("confidence", 0),
        meal_type_ai=data.get("mealType", ""),
        serving_size=data.get("servingSize", ""),
        health_score=data.get("healthScore", 0),
        health_tips=data.get("healthTips", []),
        warnings=data.get("warnings", []),
        tags=data.get("tags", [])
    )

    db.session.add(analysis)
    db.session.commit()

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
    "meal_type": analysis.meal_type_ai,

    "calories": analysis.calories,
    "protein": analysis.protein,
    "carbs": analysis.carbs,
    "fat": analysis.fat,
    "fiber": analysis.fiber,
    "sugar": analysis.sugar,
    "sodium": analysis.sodium,

    "vitamins": analysis.vitamin_data,
    "minerals": analysis.mineral_data,

    "confidence": analysis.confidence,
    "mealTypeAI": analysis.meal_type_ai,
    "servingSize": analysis.serving_size,
    "healthScore": analysis.health_score,
    "healthTips": analysis.health_tips,
    "warnings": analysis.warnings,
    "tags": analysis.tags,
    "image_url": meal.image_url,

    "created_at": meal.created_at
})

    return jsonify(history)


@food_bp.route("/history/<int:meal_id>", methods=["DELETE"])
@jwt_required()
def delete_meal(meal_id):

    user_id = get_jwt_identity()

    meal = Meal.query.filter_by(
        id=meal_id,
        user_id=user_id
    ).first()

    if not meal:
        return jsonify({
            "message": "Meal not found"
        }), 404

    analysis = NutritionAnalysis.query.filter_by(
        meal_id=meal.id
    ).first()

    if analysis:
        db.session.delete(analysis)
        db.session.commit()

    db.session.delete(meal)

    db.session.commit()

    return jsonify({
        "message": "Meal deleted successfully"
    })




@food_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    selected_date = request.args.get("date")
    selected_weekday = request.args.get("weekday")

    user_id = get_jwt_identity()

    query = Meal.query.filter_by(user_id=user_id)

    today = datetime.utcnow().date()

    if selected_date:

     selected_date = datetime.strptime(
        selected_date,
        "%Y-%m-%d"
     ).date()

     query = query.filter(
        db.func.date(Meal.created_at) == selected_date
     )

    elif selected_weekday:

      weekday_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
      }

      current_week_start = today - timedelta(days=today.weekday())

      target_date = current_week_start + timedelta(
        days=weekday_map[selected_weekday]
      )

      query = query.filter(
        db.func.date(Meal.created_at) == target_date
       )

    else:

     query = query.filter(
        db.func.date(Meal.created_at) == today
    )

    meals = query.all()
   
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
    
    # today = datetime.utcnow().date()
    # week_start = today - timedelta(days=6)
    if selected_date:
      base_date = selected_date

    elif selected_weekday:
      base_date = target_date

    else:
      base_date = datetime.utcnow().date()

    week_start = base_date - timedelta(days=base_date.weekday())
    week_end = week_start + timedelta(days=6)
    weekly_meals = (
    Meal.query.filter_by(user_id=user_id)
    .filter(
        db.func.date(Meal.created_at) >= week_start,
        db.func.date(Meal.created_at) <= week_end
    )
    .all()
)

    tracked_days = set()

    weekly_calories = 0
    weekly_protein = 0

    for meal in meals:

      analysis = NutritionAnalysis.query.filter_by(
        meal_id=meal.id
    ).first()

      if analysis:
            
            


            

            total_calories += analysis.calories or 0
            total_protein += analysis.protein or 0
            total_carbs += analysis.carbs or 0
            total_fat += analysis.fat or 0
            total_fiber += analysis.fiber or 0
            total_sugar += analysis.sugar or 0
            total_sodium += analysis.sodium or 0

            
            health_scores.append(analysis.health_score or 0)

            # print("image url from db :", meal.image_url)
            recent_meals.append({
                "meal_name": meal.meal_name,
                "calories": analysis.calories,
                "protein": analysis.protein,
                "image_url": meal.image_url
            })

    for meal in weekly_meals:

      analysis = NutritionAnalysis.query.filter_by(
        meal_id=meal.id
    ).first()

      if analysis:

        tracked_days.add(meal.created_at.date())

        weekly_calories += analysis.calories or 0
        weekly_protein += analysis.protein or 0
        day_index = meal.created_at.weekday()

        weekly_data[day_index]["calories"] += analysis.calories or 0
        weekly_data[day_index]["protein"] += analysis.protein or 0


        

    avg_health_score = (
        round(sum(health_scores) / len(health_scores))
        if health_scores
        else 0
)
    
    days_tracked = len(tracked_days)

    if days_tracked > 0:

        avg_calories = round(
           weekly_calories / days_tracked
        )

        avg_protein = round(
           weekly_protein / days_tracked
        )

    else:

         avg_calories = 0
         avg_protein = 0

   

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

        "health_score": avg_health_score,


        "avg_calories": avg_calories,
        "avg_protein": avg_protein,
        "days_tracked": days_tracked,




        
    })
