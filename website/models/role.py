from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Role(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(200))
    display_name = db.Column(db.String(200))
    
    def __repr__(self) -> str:
        return f"Role | {self.display_name}"
    
    @staticmethod
    def get_by_system_name(name) -> "Role":
        return db.session.scalars(db.select(Role).where(Role.system_name == name)).first()
    
    def get_info_for_admin(self) -> dict:
        return {
            "system_name": self.system_name,
            "display_name": self.display_name,
            "number_of_users": len(self.users)
        }
    def get_info_for_jmenovani(self) -> dict:
        return {
            "system_name": self.system_name,
            "display_name": self.display_name,
        }