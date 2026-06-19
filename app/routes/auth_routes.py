from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/health")
def health():

    return {
        "message":"NutriVision API Running"
    }