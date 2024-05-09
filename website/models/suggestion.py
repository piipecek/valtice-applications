from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Suggestion(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(2000))
    state = db.Column(db.String(2000), default="zatím neřešené")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    def __repr__(self) -> str:
        return f"Suggestion | {self.value}"

    def info_for_guest(self) -> dict:
        return {
            "author": self.author.email if self.author else "Anonym",
            "value": self.value,
            "state": self.state
        }
        
    def info_for_admin(self) -> dict:
        return {
            "author": self.author.email if self.author else "Anonym",
            "value": self.value,
            "state": self.state,
            "id": self.id
        }