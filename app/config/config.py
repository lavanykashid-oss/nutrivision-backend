from datetime import timedelta
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "nutrivision-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "nutrivision-jwt-secret-key"
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)