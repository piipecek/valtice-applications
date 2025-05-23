import json
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import current_user, logout_user
from website.models.trida import Trida
from website.models.billing import Billing
from website.models.user import User
from website.models.meal import Meal
from website.models.role import Role
from website.helpers.get_roles import get_roles
from website.helpers.require_role import require_role_system_name_on_current_user
from website.helpers.settings_manager import set_primary_classes_start_date_and_time, set_secondary_classes_start_date_and_time, set_applications_end_date_and_time, set_cz_frontpage_text, set_en_frontpage_text, toggle_user_lock_state, toggle_user_calculations_state, set_both_capacities, set_bank_details
from website.helpers.export import export
from website.helpers.end_of_issem_manager import end_of_issem
from website.helpers.logger import log, get_logs_for_browser
from website.paths import logo_cz_path, logo_en_path
from werkzeug.security import generate_password_hash
from website.mail_handler import mail_sender
import sqlalchemy

org_views = Blueprint("org_views",__name__)


@org_views.route("/", methods=["GET"])
@org_views.route("/settings", methods=["GET","POST"])
@require_role_system_name_on_current_user("organiser")
def settings():
    if request.method == "GET":
        return render_template("organizator/settings.html", roles=get_roles(current_user))
    else:
        if request.form.get("novy_ucastnik"):
            email = request.form.get("email")
            password = request.form.get("password")
            if User.get_by_email(email):
                flash("Uživatel s tímto emailem už existuje.", category="error")
                return redirect(url_for("org_views.settings"))
            if not all([email, password]):
                flash("Nebyl vyplněn email nebo heslo.", category="error")
                return redirect(url_for("org_views.settings"))
            u = User(email = email, password = generate_password_hash(password, method='scrypt'))
            if request.form.get("is_tutor"):
                u.roles.append(Role.get_by_system_name("tutor"))
            if request.form.get("email_verified"):
                u.confirmed_email = True
            if request.form.get("require_password_change"):
                u.must_change_password_upon_login = True
            u.update()
            flash("Uživatel byl vytvořen", category="success")
            return redirect(url_for("org_views.uprava_ucastnika", id=u.id))
        elif request.form.get("nova_trida"):
            t = Trida(short_name_cz=request.form.get("short_name"))
            t.update()
            id = t.id
            return redirect(url_for("org_views.uprava_tridy", id=id))
        elif request.form.get("nove_jidlo"):
            m = Meal()
            m.type = request.form.get("type")
            m.location = request.form.get("location")
            m.is_vegetarian = request.form.get("is_vegetarian") == "ano"
            try:
                m.update()
            except sqlalchemy.exc.IntegrityError:
                flash("Jídlo s těmito parametry už existuje.", category="error")
                return redirect(url_for("org_views.settings"))
            id = m.id
            flash("Jídlo bylo vytvořeno", category="success")
            return redirect(url_for("org_views.detail_jidla", id=id))
        elif request.form.get("export"):
            bytes = export()
            return send_file(bytes, as_attachment=True, download_name="export.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        elif request.form.get("dates"):
            primary_classes_start_date = request.form.get("primary_classes_start_date")
            primary_classes_start_time = request.form.get("primary_classes_start_time")
            secondary_classes_start_date = request.form.get("secondary_classes_start_date")
            secondary_classes_start_time = request.form.get("secondary_classes_start_time")
            applications_end_date = request.form.get("applications_end_date")
            applications_end_time = request.form.get("applications_end_time")
            if not all([primary_classes_start_date, primary_classes_start_time, secondary_classes_start_date, secondary_classes_start_time, applications_end_date, applications_end_time]):
                flash("Nebyl vyplněn datum nebo čas jednoho z termínů.", category="error")
                return redirect(url_for("org_views.settings"))
            else:
                set_primary_classes_start_date_and_time(primary_classes_start_date, primary_classes_start_time)
                set_secondary_classes_start_date_and_time(secondary_classes_start_date, secondary_classes_start_time)
                set_applications_end_date_and_time(applications_end_date, applications_end_time)
                flash("Datum a čas začátku přihlášek do tříd byl změněn.", category="success")
                return redirect(url_for("org_views.settings"))
        elif request.form.get("nahrat_logo_cz"):
            if "logo_cz" in request.files and request.files["logo_cz"].filename:
                logo_cz = request.files["logo_cz"]
                logo_cz.save(logo_cz_path())
                flash("Logo bylo nahráno", category="success")
            else:
                flash("Soubor nebyl nahrán", category="error")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("nahrat_logo_en"):
            if "logo_en" in request.files and request.files["logo_en"].filename:
                logo_en = request.files["logo_en"]
                logo_en.save(logo_en_path())
                flash("Logo bylo nahráno", category="success")
            else:
                flash("Soubor nebyl nahrán", category="error")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("text_cz") is not None: # aby to vzalo i prazdny
            set_cz_frontpage_text(request.form.get("cz_frontpage_text"))
            flash("Text byl změněn", category="success")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("text_en") is not None: # aby to vzalo i prazdny
            set_en_frontpage_text(request.form.get("en_frontpage_text"))
            flash("Text byl změněn", category="success")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("toggle_lock"):
            new_state = toggle_user_lock_state()
            for u in User.get_all():
                u.is_locked = new_state
                u.update()
            flash("Stav uzamčení uživatelů byl změněn", category="success")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("toggle_calculations"):
            state = toggle_user_calculations_state()
            log("Nastavení samostatného odesílání kalkulací bylo změněno na " + str(state))
            flash("Stav uzamčení uživatelů byl změněn", category="success")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("capacity"):
            set_both_capacities(request.form.get("vs_capacity"), request.form.get("gym_capacity")) 
            flash("Kapacity byly změněny", category="success")
            return redirect(url_for("org_views.settings")) 
        elif request.form.get("end_of_issem"):
            end_of_issem()
            flash("Konec ročníku úspěšně proveden, těšíme se za rok!", category="success")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("bank_details_button"):
            set_bank_details(request)
            flash("Bankovní údaje byly uloženy.", category="success")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("logs"):
            return get_logs_for_browser()
        elif request.form.get("ubytko_internat"):
            return User.get_fronta_na_internat()
        else:
            return request.form.to_dict()
    
    
@org_views.route("/detail_ucastnika/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("organiser")
def detail_ucastnika(id:int):
    u = User.get_by_id(id)
    if request.method == "GET":
        if u is None:
            flash("Uživatel s tímto ID neexistuje", category="error")
            return redirect(url_for("org_views.seznam_ucastniku"))
        return render_template("organizator/detail_ucastnika.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("zaregistrovat"):
            u.datetime_registered = datetime.now()
            u.update()
            flash("Uživatel byl zaregistrován", category="success")
            return redirect(url_for("org_views.detail_ucastnika", id=id))
        elif request.form.get("edit_button"):
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("log_in_as"):
            logout_user()
            u.login()
            flash(f"Jste přihlášen jako {u.get_full_name('cz')}. Pro pokračování s původním účtem se odhlašte a znovu přihlašte.", category="success")
            return redirect(url_for("user_views.account"))
        elif lang := request.form.get("send_calc"):
            if u.parent:
                target = u.parent.email
            else:
                target = u.email
            if lang == "cz":
                mail_sender(mail_identifier="send_calculation", target=target, data=u.info_for_calculation_email())
            else:
                mail_sender(mail_identifier="en_send_calculation", target=target, data=u.info_for_en_calculation_email())
            u.datetime_calculation_email = datetime.now()
            u.update()
            flash("E-mail s platebními údaji byl odeslán", category="success")
            return redirect(url_for("org_views.detail_ucastnika", id=id))
        return request.form.to_dict()
    
    
@org_views.route("/uprava_ucastnika/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("editor")
def uprava_ucastnika(id:int):
    if request.method == "GET":
        if User.get_by_id(id) is None:
            flash("Uživatel s tímto ID neexistuje", category="error")
            return redirect(url_for("org_views.seznam_ucastniku"))
        return render_template("organizator/uprava_ucastnika.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("save"):
            u = User.get_by_id(id)
            
            if request.form.get("parent_email"):
                if parent := User.get_by_email(request.form.get("parent_email")):
                    u.parent = parent
                else:
                    flash("Rodič s tímto emailem neexistuje", category="error")
            
            try:
                u.nacist_zmeny_z_org_requestu(request)
                flash("Změny byly uloženy", category="success")
                return redirect(url_for("org_views.detail_ucastnika", id=id))
            except sqlalchemy.exc.IntegrityError as e:
                flash("Nastala chyba při ukládání uživatele, žádná data se neuložila, kontaktujte vývojáře:" + str(e), category="error")
                return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("zrusit_registraci"):
            u = User.get_by_id(id)
            u.datetime_registered = None
            u.update()
            flash("Registrace byla zrušena", category="success")
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("registrovat_nyni"):
            u = User.get_by_id(id)
            u.datetime_registered = datetime.now()
            u.update()
            flash("Uživatel byl zaregistrován", category="success")
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("zpet"):
            return redirect(url_for("org_views.detail_ucastnika", id=id))
        elif request.form.get("delete"):
            User.get_by_id(id).delete()
            flash("Uživatel byl smazán", category="success")
            return redirect(url_for("org_views.seznam_ucastniku"))
        elif request.form.get("remove_parent"):
            u = User.get_by_id(id)
            u.parent_id = None
            u.update()
            flash("Rodič byl odebrán", category="success")
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("send_cz_reset_email"):
            u = User.get_by_id(id)
            mail_sender(mail_identifier="reset_password", target=u.email, data=u.get_reset_token())
            flash("E-mail s odkazem na změnu hesla byl odeslán", category="success")
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("send_en_reset_email"):
            u = User.get_by_id(id)
            mail_sender(mail_identifier="en_reset_password", target=u.email, data=u.get_reset_token())
            flash("E-mail s odkazem na změnu hesla byl odeslán", category="success")
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        return request.form.to_dict()
    
    
@org_views.route("/seznam_ucastniku", methods=["GET","POST"])
@require_role_system_name_on_current_user("organiser")
def seznam_ucastniku():
    if request.method == "GET":
        return render_template("organizator/seznam_ucastniku.html", roles=get_roles(current_user))
    else:
        return request.form.to_dict()
    

@org_views.route("/seznam_uctu", methods=["GET","POST"])
@require_role_system_name_on_current_user("organiser")
def seznam_uctu():
    if request.method == "GET":
        return render_template("organizator/seznam_uctu.html", roles=get_roles(current_user))
    else:
        return request.form.to_dict()
    
    
@org_views.route("/seznam_trid", methods=["GET","POST"])
@require_role_system_name_on_current_user("organiser")
def seznam_trid():
    if request.method == "GET":
        return render_template("organizator/seznam_trid.html", roles=get_roles(current_user))
    else:
        if id := request.form.get("trida"):
            return redirect(url_for("org_views.detail_tridy", id=id))
        else:
            return request.form.to_dict()


@org_views.route("/detail_tridy/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("organiser")
def detail_tridy(id:int):
    if request.method == "GET":
        return render_template("organizator/detail_tridy.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("upravit"):
            return redirect(url_for("org_views.uprava_tridy", id=id))
        else:
            return request.form.to_dict()
        

@org_views.route("/uprava_tridy/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("editor")
def uprava_tridy(id:int):
    trida = Trida.get_by_id(id)
    if trida is None:
        flash("Třída s tímto ID neexistuje", category="error")
        return redirect(url_for("org_views.seznam_trid"))
    if request.method == "GET":
        return render_template("organizator/uprava_tridy.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("save"):
            t = Trida.get_by_id(id)
            t.nacist_zmeny_z_requestu(request)
            flash("Změny byly uloženy", category="success")
            return redirect(url_for("org_views.detail_tridy", id=id))
        elif request.form.get("delete"):
            t = Trida.get_by_id(id)
            t.delete()
            flash("Třída byla smazána", category="success")
            return redirect(url_for("org_views.seznam_trid"))
        else:
            return request.form.to_dict()
    

@org_views.route("/ceny", methods=["GET","POST"])
@require_role_system_name_on_current_user("editor")
def ceny():
    if request.method == "GET":
        return render_template("organizator/ceny.html", roles=get_roles(current_user))
    else:
        if request.form.get("ulozit"):
            for cena in Billing.get_all():
                try:
                    cena.czk = float(request.form.get(f"{cena.id}_czk").replace(",","."))
                    cena.eur = float(request.form.get(f"{cena.id}_eur").replace(",","."))
                except ValueError:
                    flash("Některá pole nebyla zadána jako čísla.", category="error")
                    return redirect(url_for("org_views.ceny"))
                cena.update()
            flash("Ceny byly uloženy", category="success")
            return redirect(url_for("org_views.ceny"))
        else:
            return request.form.to_dict()
        
       
@org_views.route("/seznamy", methods=["GET","POST"])
@require_role_system_name_on_current_user("organiser")
def seznamy():
    if request.method == "GET":
        return render_template("organizator/seznamy.html", roles=get_roles(current_user))
    else:
        if request.form.get("ucel") == "excel":
            result = json.loads(request.form.get("data"))
            bytes = User.vytvorit_xlsx_seznam(result)
            return send_file(bytes, as_attachment=True, download_name="seznam.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        elif request.form.get("ucel") == "pdf":
            kriteria = json.loads(request.form.get("data"))
            data_pro_tabulku = User.vytvorit_seznam(kriteria)
            return render_template("organizator/pdf_seznam.html", data = json.dumps(data_pro_tabulku))
        elif request.form.get("ucel") == "view":
            result = json.loads(request.form.get("result"))
            data_pro_tabulku = User.vytvorit_seznam(result)
            return json.dumps(data_pro_tabulku)
        else:
            return request.form.to_dict()


@org_views.route("/organizatori", methods=["GET", "POST"])
@require_role_system_name_on_current_user("admin")
def organizatori():
    if request.method == "GET":
        return render_template("organizator/organizatori.html", roles=get_roles())
    else:
        return request.form.to_dict()
        
    
@org_views.route("/udelit_role/<int:id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("admin")
def udelit_role(id):
    if request.method == "GET":
        if id in [u.id for u in User.get_all()]:
            u = User.get_by_id(id)
            return render_template("organizator/udelit_role.html", roles=get_roles(), id=id, email=u.email)
        else:
            flash("Uživatel s tímhle ID neexistuje.", category="error")
            return redirect(url_for("org_views.edit_users"))
    else:
        if nove_role := request.form.get("nove_role"):
            nove_role_objekty = [Role.get_by_system_name(r) for r in json.loads(nove_role)]
            user = User.get_by_id(id)
            if user.roles == nove_role_objekty:
                pass
            else:
                user.roles = nove_role_objekty
                user.update()
            if Role.get_by_system_name("tutor") not in user.roles:
                user.taught_classes = []
                user.update()
            flash("Role byly upraveny.", category="success")
            return redirect(url_for("org_views.organizatori", id=id))
        else:    
            return request.form.to_dict()
    
@org_views.route("/docs")
@require_role_system_name_on_current_user("organiser")
def docs():
    return render_template("organizator/docs.html", roles=get_roles(), admins = ", ".join([u.email for u in User.get_all() if Role.get_by_system_name("admin") in u.roles]))


@org_views.route("/tutor", methods=["GET", "POST"])
@require_role_system_name_on_current_user("tutor")
def tutor():
    if request.method == "GET":
        return render_template("organizator/cz_tutor.html", roles=get_roles())
    else:
        return request.form.to_dict()
    
    
@org_views.route("/en_tutor", methods=["GET", "POST"])
@require_role_system_name_on_current_user("tutor")
def en_tutor():
    if request.method == "GET":
        return render_template("organizator/en_tutor.html", roles=get_roles())
    else:
        return request.form.to_dict()
    

@org_views.route("/seznam_lektoru")
@require_role_system_name_on_current_user("organiser")
def seznam_lektoru():
    return render_template("organizator/seznam_lektoru.html", roles=get_roles())


@org_views.route("/seznam_jidel")
@require_role_system_name_on_current_user("organiser")
def seznam_jidel():
    return render_template("organizator/seznam_jidel.html", roles=get_roles())


@org_views.route("/detail_jidla/<int:id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("organiser")
def detail_jidla(id:int):
    if request.method == "GET":
        return render_template("organizator/detail_jidla.html", id=id, roles=get_roles())
    else:
        return request.form.to_dict()


@org_views.route("/uprava_jidla/<int:id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("editor")
def uprava_jidla(id:int):
    if request.method == "GET":
        return render_template("organizator/uprava_jidla.html", id=id, roles=get_roles())
    else:
        if request.form.get("save"):
            m = Meal.get_by_id(id)
            m.type = request.form.get("type")
            m.location = request.form.get("location")
            m.is_vegetarian = request.form.get("is_vegetarian") == "ano"
            try:
                m.update()
            except sqlalchemy.exc.IntegrityError:
                flash("Jídlo s těmito parametry už existuje.", category="error")
                return redirect(url_for("org_views.uprava_jidla", id=id))
            flash("Jídlo bylo upraveno", category="success")
            return redirect(url_for("org_views.detail_jidla", id=id))
        elif request.form.get("delete"):
            Meal.get_by_id(id).delete()
            flash("Jídlo bylo smazáno", category="success")
            return redirect(url_for("org_views.seznam_jidel"))
        else:
            return request.form.to_dict()
