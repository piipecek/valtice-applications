from website.models.valtice_trida import Valtice_trida
import json
from flask import Blueprint
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.valtice_ucastnik import Valtice_ucastnik

valtice_api = Blueprint("valtice_api", __name__)


@require_role_system_name_on_current_user("valtice_org")
@valtice_api.route("/tridy_long_names_ids", methods=["GET"])
def tridy_long_names_ids():
    return json.dumps(sorted([trida.get_short_name_id_for_seznam() for trida in Valtice_trida.get_all()], key=lambda x: x["short_name"]))


@valtice_api.route("/ucastnici")
@require_role_system_name_on_current_user("valtice_org")
def ucastnici():
    return json.dumps(sorted([u.info_pro_seznam() for u in Valtice_ucastnik.get_all()], key=lambda x: x["prijmeni"]))


@valtice_api.route("/ucastnik/<int:id>")
@require_role_system_name_on_current_user("valtice_org")
def ucastnik(id: int):
    return json.dumps(Valtice_ucastnik.get_by_id(id).info_pro_detail())

@valtice_api.route("/trida/<int:id>")
@require_role_system_name_on_current_user("valtice_org")
def trida(id: int):
    return json.dumps(Valtice_trida.get_by_id(id).info_pro_detail())