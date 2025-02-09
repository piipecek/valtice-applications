import json
from flask import Blueprint
from flask_login import current_user
user_api = Blueprint("user_api", __name__)


@user_api.route("/ucet", methods=["GET"])
def ucet():
    return json.dumps(current_user.info_pro_user_detail())
