from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.password import hash_password, verify_password
from flask_jwt_extended import create_access_token

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

        user = User(
            full_name=data["full_name"],
            email=data["email"],
            password_hash=hash_password(data["password"])
        )

        UserRepository.create_user(user)

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
    