class Config:

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:LK%402005@localhost:5432/nutrivision"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "nutrivision-secret-key"

    JWT_SECRET_KEY = "nutrivision-jwt-secret-key"