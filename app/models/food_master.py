from app.config.database import db


class FoodMaster(db.Model):

    __tablename__ = "food_master"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

   

    parameter_id = db.Column(
        db.Integer,
        db.ForeignKey("parameter_master.id"),
        nullable=False
    )

    condition = db.Column(
        db.String(20),
        nullable=False
    )
    # Low / High

    food_name = db.Column(
        db.String(150),
        nullable=False
    )

    meal_type = db.Column(
        db.String(50),
        nullable=True
    )
    # Breakfast
    # Lunch
    # Dinner
    # Snack

    reason = db.Column(
        db.Text,
        nullable=True
    )

    priority = db.Column(
        db.Integer,
        default=1
    )

    parameter = db.relationship(
        "ParameterMaster",
        backref="food_recommendations"
    )