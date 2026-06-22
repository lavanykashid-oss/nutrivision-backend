from flask import Blueprint, request, jsonify

food_bp = Blueprint(
    "food",
    __name__
)


@food_bp.route("/analyze",methods=["POST"])
def analyze_food():

    image = request.files.get("image")

    food_name = request.form.get("food_name")

    print("Image:", image)
    print("Food Name:", food_name)

    return jsonify({
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
    })