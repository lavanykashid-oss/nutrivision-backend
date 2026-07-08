from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.meal import Meal
from app.models.nutrition_analysis import NutritionAnalysis


from app.config.database import db
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.services.ai_service import AIService

from app.models.user import User
from app.models.user_goal import UserGoal


coach_bp = Blueprint(
    "coach",
    __name__
)

@coach_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():

    data = request.get_json()

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    goal = UserGoal.query.filter_by(
        user_id=user_id
    ).first()

    meals = Meal.query.filter_by(user_id=user_id).all()

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_fiber = 0
    total_sugar = 0
    total_sodium = 0

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

    message = data.get("message", "")
    session_id = data.get("session_id")

    if session_id:

        session = ChatSession.query.filter_by(
            id=session_id,
            user_id=user_id
        ).first()

        if not session:
            return jsonify({
                "message": "Session not found"
            }), 404

    else:

        session = ChatSession(
            user_id=user_id,
            title=message[:40]
        )

        db.session.add(session)
        db.session.commit()

    previous_messages = (
        ChatMessage.query
        .filter_by(session_id=session.id)
        .order_by(ChatMessage.created_at.asc())
        .limit(10)
        .all()
    )
    conversation_history = ""

    for msg in previous_messages:

        if msg.role == "user":
            conversation_history += f"User: {msg.message}\n"

        else:
             conversation_history += f"Coach: {msg.message}\n"

    

    prompt = f"""
You are NutriVision AI, an expert nutrition coach.

==========================
USER PROFILE
==========================

Name: {user.full_name}

Age: {user.age}

Weight: {user.weight} kg

Goal: {goal.goal_type if goal else "Not specified"}

==========================
NUTRITION SUMMARY
==========================

Calories: {total_calories}

Protein: {total_protein} g

Carbohydrates: {total_carbs} g

Fat: {total_fat} g

Fiber: {total_fiber} g

Sugar: {total_sugar} g

Sodium: {total_sodium} mg

==========================
PREVIOUS CONVERSATION
==========================

{conversation_history}

==========================
CURRENT QUESTION
==========================

{message}

Instructions:

- Personalize every response.
- Remember previous messages.
- Give advice according to the user's goal.
- Keep responses under 150 words.
- Use bullet points when helpful.
- Never invent nutrition values.
- Motivate the user.
"""

    user_message = ChatMessage(
        session_id=session.id,
        role="user",
        message=message
    )

    db.session.add(user_message)
    db.session.commit()

    try:

        reply = AIService.generate_text(prompt)

        ai_message = ChatMessage(
            session_id=session.id,
            role="ai",
            message=reply
        )

        db.session.add(ai_message)
        db.session.commit()

    except Exception as e:

        print(e)

        reply = "Sorry, I couldn't generate a response right now."

    return jsonify({
        "reply": reply,
        "session_id": session.id
    })

@coach_bp.route("/sessions", methods=["GET"])
@jwt_required()
def get_sessions():

    user_id = get_jwt_identity()

    sessions = ChatSession.query.filter_by(
        user_id=user_id
    ).order_by(ChatSession.updated_at.desc()).all()

    data = []

    for session in sessions:

        last_message = ChatMessage.query.filter_by(
            session_id=session.id
        ).order_by(ChatMessage.created_at.desc()).first()

        data.append({
            "id": session.id,
            "title": session.title,
            "preview": last_message.message[:60] if last_message else "",
            "created_at": session.created_at
        })

    return jsonify(data)

@coach_bp.route("/session/<int:session_id>", methods=["GET"])
@jwt_required()
def get_chat(session_id):

    user_id = get_jwt_identity()

    session = ChatSession.query.filter_by(
        id=session_id,
        user_id=user_id
    ).first()

    if not session:
        return jsonify({
            "message": "Session not found"
        }), 404

    messages = ChatMessage.query.filter_by(
        session_id=session.id
    ).order_by(ChatMessage.created_at.asc()).all()

    data = []

    for msg in messages:

        data.append({
            "id": msg.id,
            "role": msg.role,
            "text": msg.message,
            "timestamp": msg.created_at
        })

    return jsonify(data)



@coach_bp.route("/session/<int:session_id>", methods=["DELETE"])
@jwt_required()
def delete_session(session_id):

    user_id = get_jwt_identity()

    session = ChatSession.query.filter_by(
        id=session_id,
        user_id=user_id
    ).first()

    if not session:
        return jsonify({
            "message": "Session not found"
        }), 404

    db.session.delete(session)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Chat deleted successfully"
    })
