from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Meal_order(Common_methods_db_model):
    __tablename__ = "meal_order"
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="meal_orders")
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"))
    meal = db.relationship("Meal", back_populates="meal_orders")
    
    
    __table_args__ = (
        db.UniqueConstraint("user_id", "meal_id", name="unique_meal_order_constraint"),
    )
    
    
    def __lt__(self, other):
        return self.meal < other.meal


    def __gt__(self, other):
        return self.meal > other.meal
    
    
    def get_by_user_id_and_meal_id(user_id, meal_id):
        return db.session.scalars(db.select(Meal_order).where(Meal_order.user_id == user_id, Meal_order.meal_id == meal_id)).first()
    