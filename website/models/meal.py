from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Meal(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200)) # breakfast, lunch, dinner
    location = db.Column(db.String(200)) # vs/zs
    is_vegetarian = db.Column(db.Boolean, default=False)
    
    meal_orders = db.relationship("Meal_order", back_populates="meal")
    