from flask import Blueprint, request
from website.models.user import User
from website.helpers.settings_manager import get_cz_frontpage_text, get_en_frontpage_text
import json

guest_api = Blueprint("guest_api", __name__)

@guest_api.route("/get_cz_text")
def get_cz_text():
    return get_cz_frontpage_text()

@guest_api.route("/get_en_text")
def get_en_text():
    return get_en_frontpage_text()

@guest_api.route("/email_odpovedne", methods=["POST"])
def email_odpvedne():
    # checks, if the email is available
    # returns 200 if user exists and has .parent = None and has .is_under_16 = False
    # returns 409 with apopropriate message if any of the above is not true
    
    if request.json["email"] == "":
        return json.dumps({
            "message_cz": "E-mail odpovědné osoby nemůže být prázdný.",
            "message_en": "E-mail of the responsible person cannot be empty."
            }), 409
    u = User.get_by_email(request.json["email"])
    if u is None:
        return json.dumps({
            "message_cz": "E-mail odpovědné osoby není v systému registrován",
            "message_en": "The e-mail of the responsible person is not registered in the system."
            }), 409
    response = u.is_valid_parent()
    return json.dumps({
        "message_cz": response["message_cz"],
        "message_en": response["message_en"],
        }), response["status"]
    