import json
from flask import Blueprint
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.trida import Trida
from website.models.billing import Billing
from website.models.user import User
from website.helpers.settings_manager import get_settings
import czech_sort
org_api = Blueprint("org_api", __name__)


@require_role_system_name_on_current_user("organizator")
@org_api.route("/tridy_long_names_ids", methods=["GET"])
def tridy_long_names_ids():
    return json.dumps(sorted([trida.get_short_name_id_for_seznam() for trida in Trida.get_all()], key=lambda x: x["short_name"]))


@org_api.route("/ucastnici")
@require_role_system_name_on_current_user("organizator")
def ucastnici():
    sorted_users = sorted(User.get_all(), key=lambda u: czech_sort.key(u.info_pro_seznam()["prijmeni"]))
    return json.dumps([u.info_pro_seznam() for u in sorted_users])


@org_api.route("/ucastnik/<int:id>")
@require_role_system_name_on_current_user("organizator")
def ucastnik(id: int):
    return json.dumps(User.get_by_id(id).info_pro_detail())

@org_api.route("/uprava_ucastnika/<int:id>")
@require_role_system_name_on_current_user("organizator")
def uprava_ucastnika(id: int):
    return json.dumps(User.get_by_id(id).info_pro_upravu())

@org_api.route("/tridy_pro_upravu_ucastnika")
@require_role_system_name_on_current_user("organizator")
def tridy_pro_upravu_ucastnika():
    return json.dumps(sorted([t.data_pro_upravu_ucastniku() for t in Trida.get_all()], key=lambda x: x["full_name"]))

@org_api.route("/tridy_pro_upravu_ucastnika_druhe_zdarma")
def tridy_pro_upravu_ucastnika_druhe_zdarma():
    return json.dumps(sorted([t.data_pro_upravu_ucastniku() for t in Trida.get_all() if t.je_zdarma_jako_vedlejsi], key=lambda x: x["full_name"]))

@org_api.route("/trida/<int:id>")
@require_role_system_name_on_current_user("organizator")
def trida(id: int):
    return json.dumps(Trida.get_by_id(id).info_pro_detail())

@org_api.route("/uprava_tridy/<int:id>")
@require_role_system_name_on_current_user("organizator")
def uprava_tridy(id: int):
    return json.dumps(Trida.get_by_id(id).info_pro_upravu())

@org_api.route("/tridy")
@require_role_system_name_on_current_user("organizator")
def tridy():
    return json.dumps(sorted([t.get_short_name_id_for_seznam() for t in Trida.get_all()], key=lambda x: x["short_name"]))

@org_api.route("/ceny")
@require_role_system_name_on_current_user("organizator")
def ceny():
    return json.dumps([c.get_data_for_admin() for c in Billing.get_all()])

@org_api.route("/tridy_pro_seznamy")
@require_role_system_name_on_current_user("organizator")
def tridy_pro_seznamy():
    return json.dumps(sorted([t.data_pro_seznamy() for t in Trida.get_all()], key=lambda x: x["long_name"]))

@org_api.route("/registrovanych")
@require_role_system_name_on_current_user("organizator")
def registrovanych():
    return json.dumps({"pocet": len(list(filter(lambda u: u.cas_registrace, User.get_all())))})

@org_api.route("/settings")
@require_role_system_name_on_current_user("organizator")
def settings():
    return json.dumps(get_settings())


@org_api.route("/uzivatele_pro_udeleni_roli")
@require_role_system_name_on_current_user("super_admin")
def uzivatele_pro_udeleni_roli():
    return json.dumps(User.get_seznam_pro_udileni_roli())


@org_api.route("/role_uzivatele/<int:id>")
@require_role_system_name_on_current_user("super_admin")
def role_uzivatele(id):
    return json.dumps([r.system_name for r in User.get_by_id(id).roles])


@org_api.route("/detail_usera/<int:id>")
@require_role_system_name_on_current_user("admin")
def detail_usera(id):
    return json.dumps(User.get_by_id(id).get_info_for_admin_detail_usera())