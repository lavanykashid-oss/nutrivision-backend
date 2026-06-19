from app.models.user import User
from app.config.database import db


class UserRepository:

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(user):
        db.session.add(user)
        db.session.commit()
        return user