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
from app.models.chat_message import ChatMessage
from app.models.deficiency_report import DeficiencyReport

load_dotenv()

def create_app():

    app = Flask(__name__)

    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/v1/auth"
    )

    @app.route("/")
    def home():
        return {
            "message": "NutriVision Backend Running Successfully"
        }

    return app