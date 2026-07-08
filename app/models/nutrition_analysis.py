from app.config.database import db

class NutritionAnalysis(db.Model):

    __tablename__ = "nutrition_analysis"

    id = db.Column(db.Integer, primary_key=True)

    meal_id = db.Column(
        db.Integer,
        db.ForeignKey("meals.id"),
        nullable=False
    )
    image_hash = db.Column(
    db.String(64),
    #unique=True,
    #nullable=True
    index=True
)
    perceptual_hash = db.Column(
    db.String(32),
    nullable=True,
    index=True
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

    confidence = db.Column(db.Integer)

    meal_type_ai = db.Column(db.String(50))

    serving_size = db.Column(db.String(100))

    health_score = db.Column(db.Integer)

    health_tips = db.Column(db.JSON)

    warnings = db.Column(db.JSON)

    tags = db.Column(db.JSON)

    meal = db.relationship(
    "Meal",
    back_populates="analysis"
)