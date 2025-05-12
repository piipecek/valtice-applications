import json
from flask import Blueprint, request
from flask_login import current_user, login_required
from website.models.trida import Trida
from website.models.meal import Meal
import czech_sort
from datetime import datetime

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


@user_api.route("/primary_classes_capacity", methods=["GET"])
@login_required
def primary_classes_capacity():
    tridy = Trida.get_all()
    tridy_na_vyber = []
    for trida in tridy:
        # nechávam tam třídy bez kapacity i časově exkluzivní třídy, to proto, ptotože pak mezi vedlejšíma bude chybět ta co mam jako hlavní
        if (current_user.is_under_16 and trida.age_group == "adult") or (not current_user.is_under_16 and trida.age_group == "child"):
            continue
        tridy_na_vyber.append(trida)
    return json.dumps(sorted([t.class_capacity_data() for t in tridy_na_vyber], key=lambda t: czech_sort.key(t["cz_name"])))


@user_api.route("/solo_secondary_classes_capacity", methods=["GET"])
@login_required
def solo_secondary_classes_capacity():
    # jsou tu jen tridy, ktere maji .has_capacity a maji skutecne misto diky .primary_participants + .secondary_participants
    # jejich .age_group je "adult" nebo "both"
    # current_user v ni neni jako primary
    # nejsou time exclusive
    tridy = Trida.get_all()
    tridy_na_vyber = []
    for trida in tridy:
        if not trida.has_capacity:
            continue
        if len(trida.primary_participants) + len(trida.secondary_participants) >= trida.capacity:
            continue
        if current_user in trida.primary_participants:
            continue
        if trida.age_group in ["child", "both"]:
            continue
        if trida.is_time_exclusive:
            continue
        tridy_na_vyber.append(trida)
    return json.dumps(sorted([t.class_capacity_data() for t in tridy_na_vyber], key=lambda t: czech_sort.key(t["cz_name"])))


@user_api.route("/no_capacity_secondary_classes_capacity", methods=["GET"])
@login_required
def no_capacity_secondary_classes_capacity():
    # jsou tu tridy, ktere maji .has_capacity == False
    # jejich .age_group je "adult" nebo "both"
    # current_user v ni neni jako primary
    # nejsou time exclusive
    tridy = Trida.get_all()
    tridy_na_vyber = []
    for trida in tridy:
        if trida.has_capacity:
            continue
        if current_user in trida.primary_participants:
            continue
        if trida.age_group == "child":
            continue
        if trida.is_time_exclusive:
            continue
        tridy_na_vyber.append(trida)
    return json.dumps(sorted([t.class_capacity_data() for t in tridy_na_vyber], key=lambda t: czech_sort.key(t["cz_name"])))


@user_api.route("/time_exclusive_secondary_classes_capacity", methods=["GET"])
@login_required
def time_exclusive_secondary_classes_capacity():
    # jsou tu tridy, ktere maji .is_time_exclusive == True
    # jejich .age_group neni child
    # current_user v ni neni jako primary
    tridy = Trida.get_all()
    tridy_na_vyber = []
    for trida in tridy:
        if not trida.is_time_exclusive:
            continue
        if current_user in trida.primary_participants:
            continue
        if trida.age_group == "child":
            continue
        tridy_na_vyber.append(trida)
    return json.dumps(sorted([t.class_capacity_data() for t in tridy_na_vyber], key=lambda t: czech_sort.key(t["cz_name"])))


@user_api.route("/handle_class_click", methods=["POST"])
@login_required
def handle_class_click():
    data = json.loads(request.data)
    trida = Trida.get_by_id(data["id"])

    if not current_user.is_this_year_participant:
        return json.dumps({
            "cz_status": "Nejste letošním účastníkem, nemůžete se zapisovat do tříd.",
            "en_status": "You are not this year's participant, you cannot enroll in classes."
            }), 400
    if data["state"] == "enrolled":
        if data["main_class"]:
            current_user.primary_class = None
            current_user.update()
        else:
            current_user.secondary_classes.remove(trida)
            current_user.update()
        return json.dumps({
            "cz_status": f"Úspěšně jste se odhlásili z třídy {trida.short_name_cz}.",
            "en_status": f"You have successfully unenrolled from class {trida.short_name_en}.",
            "data": trida.class_capacity_data()
        })
    elif data["state"] == "available":
        if data["main_class"]:
            if current_user in trida.secondary_participants:
                return json.dumps({
                    "cz_status": "Nelze se zapsat do této třídy, už jste v ní zapsaní jako vedlejší účastník. Nejdříve se ze třídy odhlaste.",
                    "en_status": "You cannot enroll in this class, you are already enrolled as a secondary participant. Please unenroll from this class first."
                    }), 400
            if current_user.primary_class is not None:
                return json.dumps({
                    "cz_status": "Nelze si zapsat do této třídy, už jste zapsaní do jiné hlavní třídy. Nejdříve se odhlašte z této třídy.",
                    "en_status": "You cannot enroll in this class, you are already enrolled in another main class. Please unenroll from this class first."
                    }), 400
            if trida.has_capacity and len(trida.primary_participants) + len(trida.secondary_participants) >= trida.capacity:
                return json.dumps({
                    "cz_status": "Třída je již plná, obnovte tuto stránku a zapište se do jiné.",
                    "en_status": "This class is already full, please refresh this page and enroll in another one."
                    }), 400
            trida.primary_participants.append(current_user)
            trida.update()
            current_user.datetime_class_pick = datetime.now()
            current_user.update()
            return json.dumps({
                "cz_status": f"Úspěšně jste byli zapsáni do třídy {trida.short_name_cz}.",
                "en_status": f"You have successfully enrolled in class {trida.short_name_en}.",
                "data": trida.class_capacity_data()
            })
        else:
            # klik na vedlejsi tridu
            if current_user.is_under_16:
                return json.dumps({
                        "cz_status": "Nelze se zapsat do vedlejší třídy, pokud je vám méně než 16 let.",
                        "en_status": "You cannot enroll in a secondary class if you are under 16."
                        }), 400
            if current_user in trida.primary_participants:
                return json.dumps({
                    "cz_status": "Nelze si zapst tuto vedlejší třídu, už jste v ní zapsaní jako hlavní účastník. Nejdříve se ze třídy odhlašte.",
                    "en_status": "You cannot enroll in this secondary class, you are already enrolled as a main participant. Please unenroll from this class first."
                    }), 400
            if trida.has_capacity and len(trida.primary_participants) + len(trida.secondary_participants) >= trida.capacity:
                return json.dumps({
                    "cz_status": "Třída je již plná, obnovte tuto stránku a zapište se do jiné.",
                    "en_status": "This class is already full, please refresh this page and enroll in another one."
                    }), 400
            pocet_vedlejsich = len([trida for trida in current_user.secondary_classes if not trida.is_time_exclusive])
            if pocet_vedlejsich == 2 and not trida.is_time_exclusive:
                return json.dumps({
                    "cz_status": "Nelze se zapsat do více než dvou vedlejších tříd (vyjma časově exkluzivních), nejprve se odhlašte z jedné z nich.",
                    "en_status": "You cannot enroll in more than two secondary classes (except for time exclusive ones), please unenroll from one of them first."
                    }), 400
            trida.secondary_participants.append(current_user)
            trida.update()
            return json.dumps({
                "cz_status": f"Úspěšně jste byli zapsáni do třídy {trida.short_name_cz}.",
                "en_status": f"You have successfully enrolled in class {trida.short_name_en}.",
                "data": trida.class_capacity_data()
            })
    else:
        return json.dumps({
            "cz_status": "error, nemáš se zapisovat do plný třídy nebo co",
            "en_status": "error, you should not be enrolling in a full class or something"
            }) , 400
    

@user_api.route("/jidla_pro_upravu_ucastnika")
@login_required
def jidla_pro_upravu_ucastnika():
    return json.dumps([m.data_pro_upravu_ucastnika() for m in sorted(Meal.get_all())])  


@user_api.route("/en_jidla_pro_upravu_ucastnika")
@login_required
def en_jidla_pro_upravu_ucastnika():
    return json.dumps([m.en_data_pro_upravu_ucastnika() for m in sorted(Meal.get_all())])  
