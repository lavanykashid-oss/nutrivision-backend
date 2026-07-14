
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from app.models.user import User
from app.models.user_goal import UserGoal

from google.oauth2 import id_token
from google.auth.transport import requests

from app.config.database import db
import os

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



@auth_bp.route("/google", methods=["POST"])
def google_login():

    data = request.get_json()

    credential = data.get("credential")

    if not credential:
        return jsonify({
            "success": False,
            "message": "Google credential missing"
        }), 400

    try:
        idinfo = id_token.verify_oauth2_token(
            credential,
            requests.Request(),
            os.getenv("GOOGLE_CLIENT_ID")
        )

    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid Google token"
        }), 401

    google_id = idinfo["sub"]
    email = idinfo["email"]
    name = idinfo["name"]
    picture = idinfo.get("picture")

    # ---------------------------------------
    # Check if user already exists
    # ---------------------------------------
    user = User.query.filter_by(email=email).first()

    if user:

        # Existing local account
        if user.provider == "local":

            user.provider = "google"
            user.google_id = google_id

            if picture:
                user.profile_picture = picture

            db.session.commit()

        # Existing Google account
        else:

            if picture:
                user.profile_picture = picture

            db.session.commit()

    else:
        # ---------------------------------------
        # First Google Login
        # ---------------------------------------
        user = User(
            full_name=name,
            email=email,
            provider="google",
            google_id=google_id,
            profile_picture=picture
        )

        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "success": True,
        "token": access_token,
        "new_user": user.age is None,
        "user":{
            "name": user.full_name,
            "email": user.email,
            "picture": user.profile_picture

        }
    }), 200

@auth_bp.route("/complete-profile", methods=["POST"])
@jwt_required()
def complete_profile():

    user_id = get_jwt_identity()
    data = request.get_json()

    result = AuthService.complete_profile(
        user_id,
        data
    )

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200