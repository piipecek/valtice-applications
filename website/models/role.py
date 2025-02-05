from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable

class Role(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(200))
    display_name = db.Column(db.String(200))
    
    users = db.relationship("User", secondary=user_role_jointable, back_populates="roles")
    
    _role_hiearchy = {
        "tutor": 1,
        "organiser": 2,
        "editor": 3,
        "admin": 4
    }
    
    def __repr__(self) -> str:
        return f"Role | {self.display_name}"
    
    @staticmethod
    def get_by_system_name(name) -> "Role":
        return db.session.scalars(db.select(Role).where(Role.system_name == name)).first()

    def update(self): # prepisuje update z common model
        role = Role.get_by_system_name(self.system_name)
        if role is None:
            db.session.add(self)
        else:
            role.display_name = self.display_name
        db.session.commit()

    def __lt__(self, other) -> bool:
        return self._role_hiearchy[self.system_name] < self._role_hiearchy[other.system_name]
    
    def __le__(self, other) -> bool:
        return self._role_hiearchy[self.system_name] <= self._role_hiearchy[other.system_name]
    
    def __gt__(self, other) -> bool:
        return self._role_hiearchy[self.system_name] > self._role_hiearchy[other.system_name]
    
    def __ge__(self, other) -> bool:
        return self._role_hiearchy[self.system_name] >= self._role_hiearchy[other.system_name]
    
    def __eq__(self, other) -> bool:
        return self._role_hiearchy[self.system_name] == self._role_hiearchy[other.system_name]
    
    def __ne__(self, other) -> bool:
        return self._role_hiearchy[self.system_name] != self._role_hiearchy[other.system_name]
    