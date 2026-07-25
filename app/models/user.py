from datetime import datetime
from app.config.database import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

   
    

    

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=True
    )

    google_id = db.Column(
    db.String(255),
    unique=True,
    nullable=True
)

    profile_picture = db.Column(
      db.String(500),
      nullable=True
)

    provider = db.Column(
      db.String(20),
      default="local",
      nullable=False
)

    age = db.Column(db.Integer)

    dob = db.Column(db.Date)

    # gender = db.Column(db.String(20))

    # height = db.Column(db.Float)

    weight = db.Column(db.Float)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )