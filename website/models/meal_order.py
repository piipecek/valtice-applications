from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Meal_order(Common_methods_db_model):
    __tablename__ = "meal_order"
    id = db.Column(db.Integer, primary_key=True)
    set_count = db.Column(db.Integer, default=1)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"))
    
    user = db.relationship("User", back_populates="meal_orders")
    meal = db.relationship("Meal", back_populates="meal_orders")