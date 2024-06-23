from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Cena(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(300))
    display_name = db.Column(db.String(1000))
    system_name = db.Column(db.String(100), unique=True)
    czk = db.Column(db.Float, default=0)
    eur = db.Column(db.Float, default=0)
    
    def get_data_for_admin(self) -> dict:
        return {
            "id": self.id,
            "typ": self.typ,
            "display_name": self.display_name,
            "system_name": self.system_name,
            "czk": self.czk,
            "eur": self.eur
        }