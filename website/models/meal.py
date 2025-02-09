from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_meal_jointable

class Meal(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200), default="breakfast") # breakfast, lunch, dinner
    location = db.Column(db.String(200), default="vs") # vs/zs
    is_vegetarian = db.Column(db.Boolean, default=False)
    
    users = db.relationship("User", secondary=user_meal_jointable, back_populates="meals")
    