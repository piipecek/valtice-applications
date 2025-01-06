import json
from flask import Blueprint
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.valtice_ucastnik import Valtice_ucastnik
from website.models.valtice_trida import Valtice_trida
from website.models.cena import Cena
import czech_sort
valtice_api = Blueprint("valtice_api", __name__)


@require_role_system_name_on_current_user("organizator")
@valtice_api.route("/tridy_long_names_ids", methods=["GET"])
def tridy_long_names_ids():
    return json.dumps(sorted([trida.get_short_name_id_for_seznam() for trida in Valtice_trida.get_all()], key=lambda x: x["short_name"]))


@valtice_api.route("/ucastnici")
@require_role_system_name_on_current_user("organizator")
def ucastnici():
    sorted_users = sorted(Valtice_ucastnik.get_all(), key=lambda u: czech_sort.key(u.info_pro_seznam()["prijmeni"]))
    return json.dumps([u.info_pro_seznam() for u in sorted_users])


@valtice_api.route("/ucastnik/<int:id>")
@require_role_system_name_on_current_user("organizator")
def ucastnik(id: int):
    return json.dumps(Valtice_ucastnik.get_by_id(id).info_pro_detail())

@valtice_api.route("/uprava_ucastnika/<int:id>")
@require_role_system_name_on_current_user("organizator")
def uprava_ucastnika(id: int):
    return json.dumps(Valtice_ucastnik.get_by_id(id).info_pro_upravu())

@valtice_api.route("/tridy_pro_upravu_ucastnika")
@require_role_system_name_on_current_user("organizator")
def tridy_pro_upravu_ucastnika():
    return json.dumps(sorted([t.data_pro_upravu_ucastniku() for t in Valtice_trida.get_all()], key=lambda x: x["full_name"]))

@valtice_api.route("/tridy_pro_upravu_ucastnika_druhe_zdarma")
def tridy_pro_upravu_ucastnika_druhe_zdarma():
    return json.dumps(sorted([t.data_pro_upravu_ucastniku() for t in Valtice_trida.get_all() if t.je_zdarma_jako_vedlejsi], key=lambda x: x["full_name"]))

@valtice_api.route("/trida/<int:id>")
@require_role_system_name_on_current_user("organizator")
def trida(id: int):
    return json.dumps(Valtice_trida.get_by_id(id).info_pro_detail())

@valtice_api.route("/uprava_tridy/<int:id>")
@require_role_system_name_on_current_user("organizator")
def uprava_tridy(id: int):
    return json.dumps(Valtice_trida.get_by_id(id).info_pro_upravu())

@valtice_api.route("/tridy")
@require_role_system_name_on_current_user("organizator")
def tridy():
    return json.dumps(sorted([t.get_short_name_id_for_seznam() for t in Valtice_trida.get_all()], key=lambda x: x["short_name"]))

@valtice_api.route("/ceny")
@require_role_system_name_on_current_user("organizator")
def ceny():
    return json.dumps([c.get_data_for_admin() for c in Cena.get_all()])

@valtice_api.route("/tridy_pro_seznamy")
@require_role_system_name_on_current_user("organizator")
def tridy_pro_seznamy():
    return json.dumps(sorted([t.data_pro_seznamy() for t in Valtice_trida.get_all()], key=lambda x: x["long_name"]))

@valtice_api.route("/registrovanych")
@require_role_system_name_on_current_user("organizator")
def registrovanych():
    return json.dumps({"pocet": len(list(filter(lambda u: u.cas_registrace, Valtice_ucastnik.get_all())))})