import json
from flask import Blueprint, request
from flask_login import current_user, login_required
from website.models.trida import Trida
from website.models.meal import Meal
import czech_sort

user_api = Blueprint("user_api", __name__)


@user_api.route("/ucet", methods=["GET"])
@login_required
def ucet():
    return json.dumps(current_user.info_pro_user_detail())


@user_api.route("/en_ucet", methods=["GET"])
@login_required
def en_ucet():
    return json.dumps(current_user.info_pro_en_user_detail())


@user_api.route("/uprava_uctu", methods=["GET"])
@login_required
def uprava_uctu():
    return json.dumps(current_user.info_pro_user_upravu())


@user_api.route("/en_uprava_uctu", methods=["GET"])
@login_required
def en_uprava_uctu():
    return json.dumps(current_user.info_pro_en_user_upravu())


@user_api.route("/cz_classes_capacity", methods=["GET"])
@login_required
def cz_classes_capacity():
    return json.dumps(sorted([t.class_capacity_data() for t in Trida.get_all()], key=lambda t: czech_sort.key(t["name"])))


@user_api.route("/handle_class_click", methods=["POST"])
@login_required
def handle_class_click():
    data = json.loads(request.data)
    trida = Trida.get_by_id(data["id"])
    
    if data["state"] == "enrolled":
        if data["main_class"]:
            current_user.main_class_id_priority_1 = None
            current_user.update()
        else:
            current_user.secondary_class_id = None
            current_user.update()
        return json.dumps(trida.class_capacity_data())
    elif data["state"] == "available":
        if data["main_class"]:
            if current_user in trida.secondary_participants:
                return json.dumps({"status": "Nelze si zapsat do této třídy, už jste v ní zapsaní jako vedlejší účastník. Nejdříve se ze třídy odhlašte."}), 400
            if current_user.main_class_id_priority_1 is not None:
                return json.dumps({"status": "Nelze si zapsat do této třídy, už jste zapsaní do jiné hlavní třídy. Nejdříve se odhlašte z této třídy."}), 400
            if trida.is_solo and len(trida.main_paticipants_priority_1) >= trida.capacity:
                return json.dumps({"status": "Třída je již plná, obnovte tuto stránku zapište se do jiné."}), 400
            trida.main_paticipants_priority_1.append(current_user)
            trida.update()
            return json.dumps(trida.class_capacity_data())
        else:
            if current_user in trida.main_paticipants_priority_1:
                return json.dumps({"status": "Nelze si zapst tuto vedlejší třídu, už jste v ní zapsaní jako hlavní účastník. Nejdříve se ze třídy odhlašte."}), 400
            if current_user.secondary_class_id is not None:
                return json.dumps({"status": "Nelze si zapsat do této třídy, už jste zapsaní do jiné vedlejší třídy. Nejdříve se odhlašte z této třídy."}), 400
            trida.secondary_participants.append(current_user)
            trida.update()
            return json.dumps(trida.class_capacity_data())
    else:
        return json.dumps({"status": "error, nemáš se zapisovat do plný třídy nebo co"}) , 400
    

@user_api.route("/jidla_pro_upravu_ucastnika")
@login_required
def jidla_pro_upravu_ucastnika():
    return json.dumps([m.data_pro_upravu_ucastnika() for m in sorted(Meal.get_all())])  


@user_api.route("/en_jidla_pro_upravu_ucastnika")
@login_required
def en_jidla_pro_upravu_ucastnika():
    return json.dumps([m.en_data_pro_upravu_ucastnika() for m in sorted(Meal.get_all())])  
