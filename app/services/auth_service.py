from app.models.user import User
from app.models.user_goal import UserGoal
from app.repositories.user_repository import UserRepository
from app.utils.password import hash_password, verify_password
from flask_jwt_extended import create_access_token
from app.config.database import db
from datetime import datetime


class AuthService:

    @staticmethod
    def register_user(data):

        existing_user = UserRepository.get_by_email(
            data["email"]
        )

        if existing_user:
            return {
                "success": False,
                "message": "Email already exists"
            }
        
        dob = None

        if data.get("dob"):
          dob = datetime.strptime(
          data["dob"],
          "%Y-%m-%d"
        ).date()

        user = User(
            full_name=data["full_name"],
            email=data["email"],
            password_hash=hash_password(data["password"]),
            dob=dob,
            age=data.get("age"),
            weight=data.get("weight"),
            # height=data.get("height"),
            # gender=data.get("gender")
        )

        db.session.add(user)
        db.session.flush()      # Generates user.id without committing

        goal = UserGoal(
            user_id=user.id,
            goal_type=data.get("goal")
        )

        db.session.add(goal)
        db.session.commit()

        return {
            "success": True,
            "message": "User registered successfully"
        }
    
    @staticmethod
    def login_user(data):

        user = UserRepository.get_by_email(
            data["email"]
        )

        if not user:
            return {
                "success": False,
                "message": "Invalid email or password"
            }

        if not verify_password(
            data["password"],
            user.password_hash
        ):
            return {
                "success": False,
                "message": "Invalid email or password"
            }

        token = create_access_token(
            identity=str(user.id)
        )

        return {
            "success": True,
            "message": "Login successful",
            "token": token
        }
    @staticmethod
    def complete_profile(user_id, data):

        user = User.query.get(user_id)

        if not user:
            return {
                "success": False,
                "message": "User not found"
            }

        dob = None
        if data.get("dob"):
            dob = datetime.strptime(
                data["dob"],
                "%Y-%m-%d"
            ).date()

        user.dob = dob
        user.age = data.get("age")
        user.weight = data.get("weight")

        # Update goal
        goal = UserGoal.query.filter_by(user_id=user.id).first()

        if goal:
            goal.goal_type = data.get("goal")
        else:
            goal = UserGoal(
                user_id=user.id,
                goal_type=data.get("goal")
            )
            db.session.add(goal)

        db.session.commit()

        return {
            "success": True,
            "message": "Profile completed successfully"
        }
