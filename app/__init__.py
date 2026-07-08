from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.config.database import db
from app.routes.auth_routes import auth_bp
from flask_migrate import Migrate

from app.models.user import User
from app.models.user_goal import UserGoal
from app.models.meal import Meal
from app.models.nutrition_analysis import NutritionAnalysis
from app.models.daily_progress import DailyProgress
from app.models.deficiency_report import DeficiencyReport
from flask_jwt_extended import JWTManager
from app.config.config import Config
from app.routes.food_routes import food_bp
from app.routes.coach import coach_bp

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage


load_dotenv()
jwt = JWTManager()
def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)   
    
    print(os.getenv("DATABASE_URL"))
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    print("SECRET_KEY =", app.config.get("SECRET_KEY"))
    print("JWT_SECRET_KEY =", app.config.get("JWT_SECRET_KEY"))
    jwt.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/v1/auth"
    )

    app.register_blueprint(
        food_bp,
        url_prefix="/api/v1/food"
    )

    app.register_blueprint(
    coach_bp,
    url_prefix="/api/v1/coach"
)

    @app.route("/")
    def home():
        return {
            "message": "NutriVision Backend Running Successfully"
        }

    return app