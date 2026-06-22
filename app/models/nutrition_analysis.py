from app.config.database import db

class NutritionAnalysis(db.Model):

    __tablename__ = "nutrition_analysis"

    id = db.Column(db.Integer, primary_key=True)

    meal_id = db.Column(
        db.Integer,
        db.ForeignKey("meals.id"),
        nullable=False
    )

    calories = db.Column(db.Float)

    protein = db.Column(db.Float)

    fat = db.Column(db.Float)

    carbs = db.Column(db.Float)

    fiber = db.Column(db.Float)

    sugar = db.Column(db.Float)

    sodium = db.Column(db.Float)
    

    vitamin_data = db.Column(db.JSON)

    mineral_data = db.Column(db.JSON)