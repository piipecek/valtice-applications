import json
from flask import Blueprint
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.trida import Trida
from website.models.billing import Billing
from website.models.user import User
from website.models.role import Role
from website.models.meal import Meal
from website.helpers.settings_manager import get_settings
import czech_sort
from flask_login import current_user
org_api = Blueprint("org_api", __name__)


@require_role_system_name_on_current_user("organiser")
@org_api.route("/tridy_long_names_ids", methods=["GET"])
def tridy_long_names_ids():
    return json.dumps(sorted([trida.get_short_name_id_for_seznam() for trida in Trida.get_all()], key=lambda x: x["short_name"]))


@org_api.route("/seznam_ucastniku")
@require_role_system_name_on_current_user("organiser")
def seznam_ucastniku():
    sorted_users = sorted([u for u in User.get_all() if len(u.roles) == 0], key=lambda u: czech_sort.key(u.info_pro_seznam()["surname"]))
    return json.dumps([u.info_pro_seznam() for u in sorted_users])


@org_api.route("/detail_ucastnika/<int:id>")
@require_role_system_name_on_current_user("organiser")
def detail_ucastnika(id: int):
    return json.dumps(User.get_by_id(id).info_pro_detail())

@org_api.route("/uprava_ucastnika/<int:id>")
@require_role_system_name_on_current_user("organiser")
def uprava_ucastnika(id: int):
    return json.dumps(User.get_by_id(id).info_pro_upravu())

@org_api.route("/tridy_pro_upravu_ucastnika")
@require_role_system_name_on_current_user("organiser")
def tridy_pro_upravu_ucastnika():
    return json.dumps(sorted([t.data_pro_upravu_ucastniku() for t in Trida.get_all()], key=lambda x: x["full_name_cz"]))

@org_api.route("/detail_tridy/<int:id>")
@require_role_system_name_on_current_user("organiser")
def detail_tridy(id: int):
    return json.dumps(Trida.get_by_id(id).info_pro_detail())

@org_api.route("/uprava_tridy/<int:id>")
@require_role_system_name_on_current_user("organiser")
def uprava_tridy(id: int):
    return json.dumps(Trida.get_by_id(id).info_pro_upravu())

@org_api.route("/seznam_trid")
@require_role_system_name_on_current_user("organiser")
def seznam_trid():
    return json.dumps(sorted([t.info_pro_seznam_trid() for t in Trida.get_all()], key=lambda x: x["short_name"]))

@org_api.route("/ceny")
@require_role_system_name_on_current_user("organiser")
def ceny():
    return json.dumps([c.get_data_for_admin() for c in Billing.get_all()])

@org_api.route("/tridy_pro_seznamy")
@require_role_system_name_on_current_user("organiser")
def tridy_pro_seznamy():
    return json.dumps(sorted([t.data_pro_seznamy() for t in Trida.get_all()], key=lambda x: x["long_name"]))

@org_api.route("/registrovanych")
@require_role_system_name_on_current_user("organiser")
def registrovanych():
    return json.dumps({"pocet": len(list(filter(lambda u: u.datetime_registered, User.get_all())))})

@org_api.route("/settings")
@require_role_system_name_on_current_user("organiser")
def settings():
    return json.dumps(get_settings())


@org_api.route("/uzivatele_pro_udeleni_roli")
@require_role_system_name_on_current_user("admin")
def uzivatele_pro_udeleni_roli():
    return json.dumps(User.get_seznam_pro_udileni_roli())


@org_api.route("/role_uzivatele/<int:id>")
@require_role_system_name_on_current_user("admin")
def role_uzivatele(id):
    return json.dumps([r.system_name for r in User.get_by_id(id).roles])

@org_api.route("/seznam_lektoru")
@require_role_system_name_on_current_user("organiser")
def seznam_lektoru():
    tutor_role = Role.get_by_system_name("tutor")
    return json.dumps(sorted([u.info_pro_seznam_lektoru() for u in User.get_all() if tutor_role in u.roles], key=lambda x: x["surname"]))

@org_api.route("/seznam_lektoru_pro_upravu_tridy")
@require_role_system_name_on_current_user("organiser")
def seznam_lektoru_pro_upravu_tridy():
    tutor_role = Role.get_by_system_name("tutor")
    return json.dumps(User.get_seznam_pro_options_na_uprave_tridy())

@org_api.route("/cz_my_participants")
@require_role_system_name_on_current_user("tutor")
def my_participants():
    result = [
        {
            "class_name": trida.full_name_cz,
            "main_participants": [u.info_for_tutor() for u in trida.main_paticipants_priority_1],
            "secondary_participants": [u.info_for_tutor() for u in trida.secondary_participants]
        } for trida in current_user.taught_classes
    ]
    return json.dumps(result)

@org_api.route("/en_my_participants")
@require_role_system_name_on_current_user("tutor")
def my_participants_en():
    result = [
        {
            "class_name": trida.full_name_en,
            "main_participants": [u.info_for_tutor() for u in trida.main_paticipants_priority_1],
            "secondary_participants": [u.info_for_tutor() for u in trida.secondary_participants]
        } for trida in current_user.taught_classes
    ]
    return json.dumps(result)


@org_api.route("/seznam_jidel")
@require_role_system_name_on_current_user("organiser")
def seznam_jidel():
    return json.dumps([m.get_data_for_admin_seznam() for m in sorted(Meal.get_all())])


@org_api.route("/detail_jidla/<int:id>")
@require_role_system_name_on_current_user("organiser")
def detail_jidla(id: int):
    return json.dumps(Meal.get_by_id(id).info_pro_detail())


@org_api.route("/uprava_jidla/<int:id>")
@require_role_system_name_on_current_user("editor")
def uprava_jidla(id: int):
    return json.dumps(Meal.get_by_id(id).info_pro_upravu())