from app.config.database import db


class MealRecipe(db.Model):

    __tablename__ = "meal_recipe"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    meal_type = db.Column(
        db.String(50),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    foods = db.Column(
        db.Text,
        nullable=False
    )

    goal = db.Column(
    db.String(100),
    nullable=True
)

    description = db.Column(
        db.Text
    )