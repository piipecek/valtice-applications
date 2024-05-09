import json
from flask import Blueprint
from website.helpers.require_role import require_role_system_name_on_current_user
from flask_login import current_user

user_api = Blueprint("user_api", __name__)

@user_api.route("/detail_usera")
@require_role_system_name_on_current_user("user")
def detail_usera():
    return json.dumps(current_user.get_info_for_detail_usera())


@user_api.route("/jazyky")
@require_role_system_name_on_current_user("user")
def jazyky():
    return json.dumps(current_user.get_info_for_detail_usera())
