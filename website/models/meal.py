from website import db
from website.models.common_methods_db_model import Common_methods_db_model


class Meal(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200), default="breakfast") # breakfast, lunch, dinner
    location = db.Column(db.String(200), default="vs") # vs/zs
    is_vegetarian = db.Column(db.Boolean, default=False)
    
    meal_orders = db.relationship("Meal_order", back_populates="meal")
    
    __table_args__ = (
        db.UniqueConstraint("type", "location", "is_vegetarian", name="unique_meal_constraint"),
    )
    
    _type_ranks = ["breakfast", "lunch", "dinner"]
    _location_ranks = ["zs", "vs"]
    
    def __lt__(self, other):
        if self.type != other.type:
            return self._type_ranks.index(self.type) < self._type_ranks.index(other.type)
        if self.location != other.location:
            return self._location_ranks.index(self.location) < self._location_ranks.index(other.location)
        return self.is_vegetarian > other.is_vegetarian
    

    def __gt__(self, other):
        if self.type != other.type:
            return self._type_ranks.index(self.type) > self._type_ranks.index(other.type)
        if self.location != other.location:
            return self._location_ranks.index(self.location) > self._location_ranks.index(other.location)
        return self.is_vegetarian < other.is_vegetarian
    
    
    def get_data_for_admin_seznam(self):
        typ = "snídaně"
        if self.type == "lunch":
            typ = "oběd"
        elif self.type == "dinner":
            typ = "večeře"
        return {
            "id": self.id,
            "type": typ,
            "location": "základní škola" if self.location == "zs" else "vinařská škola",
            "is_vegetarian": "Ano" if self.is_vegetarian else "Ne",
            "count": sum([meal_order.count for meal_order in self.meal_orders])
        }
    
    def info_pro_detail(self):
        typ = "snídaně"
        if self.type == "lunch":
            typ = "oběd"
        elif self.type == "dinner":
            typ = "večeře"
        return {
            "type": typ,
            "location": "základní škola" if self.location == "zs" else "vinařská škola",
            "is_vegetarian": "Ano" if self.is_vegetarian else "Ne",
            "count": sum([meal_order.count for meal_order in self.meal_orders])
        }


    def info_pro_upravu(self):
        return {
            "type": self.type,
            "location": self.location,
            "is_vegetarian": "ano" if self.is_vegetarian else "ne",
        }