import json
from flask import Blueprint
from website.helpers.require_role import require_role_system_name_on_current_user
from website.logs import get_app_logs
from website.models.role import Role
from website.models.user import User

admin_api = Blueprint("admin_api", __name__)


@admin_api.route("/app_logs")
@require_role_system_name_on_current_user("admin")
def app_logs():
    return json.dumps(get_app_logs())

@admin_api.route("/uzivatele_pro_udeleni_roli")
@require_role_system_name_on_current_user("super_admin")
def uzivatele_pro_udeleni_roli():
    return json.dumps(User.get_seznam_pro_udileni_roli())

@admin_api.route("/role_uzivatele/<int:id>")
@require_role_system_name_on_current_user("super_admin")
def role_uzivatele(id):
    return json.dumps([r.system_name for r in User.get_by_id(id).roles])

@admin_api.route("/detail_usera/<int:id>")
@require_role_system_name_on_current_user("admin")
def detail_usera(id):
    return json.dumps(User.get_by_id(id).get_info_for_admin_detail_usera())