from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Billing(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(300)) # course / accommodation / food
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
    
    @staticmethod
    def get_by_system_name(system_name:str):
        return db.session.scalars(db.select(Billing).where(Billing.system_name == system_name)).first()


    def update(self): # prepsani metody z common modelu
        billing = Billing.get_by_system_name(self.system_name)
        if billing is None:
            db.session.add(self)
        else:
            billing.display_name = self.display_name
            billing.czk = self.czk
            billing.eur = self.eur
        db.session.commit()