from flask import Blueprint
from website.helpers.settings_manager import get_cz_frontpage_text, get_en_frontpage_text

guest_api = Blueprint("guest_api", __name__)

@guest_api.route("/get_cz_text")
def get_cz_text():
    return get_cz_frontpage_text()

@guest_api.route("/get_en_text")
def get_en_text():
    return get_en_frontpage_text()