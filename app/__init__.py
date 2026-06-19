from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.config.database import db
from app.routes.auth_routes import auth_bp


load_dotenv()

def create_app():

    app = Flask(__name__)

    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "postgresql://postgres:password@localhost:5432/nutrivision"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
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