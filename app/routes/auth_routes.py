
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.user_goal import UserGoal


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["POST"]
)

def register():

    data = request.get_json()
    print(data)

    result = AuthService.register_user(data)

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    result = AuthService.login_user(data)

    if not result["success"]:
        return jsonify(result), 401

    return jsonify(result), 200

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    goal = UserGoal.query.filter_by(
        user_id = user_id
    ).first()

    return jsonify({
    "name": user.full_name,
    "email": user.email,
    "goal": goal.goal_type if goal else "Not set",
    "age": user.age,
    "dob": user.dob,
    # "gender": user.gender,
    # "height": user.height,
    "weight": user.weight,
    
})