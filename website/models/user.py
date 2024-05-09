from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from website.helpers.pretty_date import pretty_datetime
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_login import UserMixin, current_user, login_user
from typing import List
import jwt

def get_roles(u: "User" = current_user) -> List[str]:
    result = []
    if u.is_authenticated:
        result.append("prihlasen")
        result.extend([r.system_name for r in u.roles])
    return result


class User(Common_methods_db_model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    last_login_datetime = db.Column(db.DateTime)
    registration_datetime = db.Column(db.DateTime, default = datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    acga_jmeno = db.Column(db.String(200))
    roles = db.relationship("Role", secondary=user_role_jointable, backref="users")
    suggestions = db.relationship("Suggestion", backref="author")
    
    def __repr__(self) -> str:
        return f"Uživatel | {self.email}"
    
    @staticmethod
    def get_by_email(email) -> "User":
        return db.session.scalars(db.select(User).where(User.email == email)).first()
        
        
    def get_reset_token(self, expires_sec=9000) -> str:
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec)
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return reset_token    
    
    
    @staticmethod
    def verify_reset_token(token) -> "User":
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return None
        return User.get_by_id(data["user_id"])
    
    @staticmethod
    def get_seznam_pro_jmenovani_adminu() -> list:
        result = {
            "admins": [],
            "users": []
        }
        for u in User.get_all():
            data = {
                "id": u.id,
                "email": u.email
            }
            if "admin" in get_roles(u):
                result["admins"].append(data)
            else:
                result["users"].append(data)
        return result
    
    def get_info_pro_seznam_useru(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "last_login_datetime": pretty_datetime(self.last_login_datetime),
            "confirmed": "Ano" if self.confirmed else "Ne"
        }
    
    def login(self):
        login_user(self, remember=True)
        self.last_login_datetime = datetime.now()
        self.update()
        
    def get_info_for_admin_detail_usera(self) -> dict:
        return [
            {
                "display_name": "ID v systému",
                "value": self.id
            },
            {
                "display_name":"E-mail",
                "value": self.email
            },
            {
                "display_name":"Ověřený e-mail",
                "value": "Ano" if self.confirmed else "Ne"
            },
            {
                "display_name":"Registrace",
                "value": pretty_datetime(self.registration_datetime)
            },
            {
                "display_name": "Poslední přihlášení",
                "value": pretty_datetime(self.last_login_datetime)
            }
        ]

        
    def get_info_for_detail_usera(self) -> dict:
        return {
            "email": self.email,
            "registration_datetime": pretty_datetime(self.registration_datetime),
            "confirmed": "Ano" if self.confirmed else "Ne"
        }