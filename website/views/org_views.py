from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import current_user
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.valtice_ucastnik import Valtice_ucastnik
from website.models.valtice_trida import Valtice_trida
from website.models.cena import Cena
from website.models.user import get_roles
from website.helpers.settings_manager import set_applications_start_date_and_time, set_applications_end_date_and_time
import csv
import json
from datetime import datetime
from io import StringIO
from website.helpers.export import export

org_views = Blueprint("org_views",__name__)

@org_views.route("/", methods=["GET"])
@org_views.route("/settings", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def settings():
    if request.method == "GET":
        return render_template("organizator/settings.html", roles=get_roles(current_user))
    else:
        if request.form.get("delete_all"):
            for u in Valtice_ucastnik.get_all():
                u.delete()
            flash("Všichni účastníci byli smazáni", category="success")
            return redirect(url_for("org_views.settings"))
        elif request.form.get("novy_ucastnik"):
            id = Valtice_ucastnik.novy_ucastnik_from_admin(jmeno = request.form.get("jmeno"), prijmeni = request.form.get("prijmeni"))
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("nova_trida"):
            v = Valtice_trida(short_name=request.form.get("short_name"))
            v.update()
            id = v.id
            return redirect(url_for("org_views.uprava_tridy", id=id))
        elif request.form.get("export"):
            bytes = export()
            return send_file(bytes, as_attachment=True, download_name="export.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        elif request.form.get("datum_cas_start"):
            applications_start_date = request.form.get("applications_start_date")
            applications_start_time = request.form.get("applications_start_time")
            if not all([applications_start_date, applications_start_time]):
                flash("Nebyl vyplněn datum nebo čas začátku přihlášek.", category="error")
                return redirect(url_for("org_views.settings"))
            else:
                set_applications_start_date_and_time(applications_start_date, applications_start_time)
                flash("Datum a čas začátku přihlášek byl změněn.", category="success")
                return redirect(url_for("org_views.settings"))
        elif request.form.get("datum_cas_end"):
            applications_end_date = request.form.get("applications_end_date")
            applications_end_time = request.form.get("applications_end_time")
            if not all([applications_end_date, applications_end_time]):
                flash("Nebyl vyplněn datum nebo čas konce přihlášek.", category="error")
                return redirect(url_for("org_views.settings"))
            else:
                set_applications_end_date_and_time(applications_end_date, applications_end_time)
                flash("Datum a čas konce přihlášek byl změněn.", category="success")
                return redirect(url_for("org_views.settings"))
        else:
            return request.form.to_dict()
    
    
@org_views.route("/ucastnik/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def ucastnik(id:int):
    if request.method == "GET":
        if Valtice_ucastnik.get_by_id(id) is None:
            flash("Uživatel s tímto ID neexistuje", category="error")
            return redirect(url_for("org_views.seznam_ucastniku"))
        return render_template("organizator/ucastnik.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("zaregistrovat"):
            u = Valtice_ucastnik.get_by_id(id)
            u.cas_registrace = datetime.now()
            u.update()
            flash("Uživatel byl zaregistrován", category="success")
            return redirect(url_for("org_views.ucastnik", id=id))
        elif request.form.get("edit_button"):
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        return request.form.to_dict()
    
# view na upravu ucastnika
@org_views.route("/uprava_ucastnika/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def uprava_ucastnika(id:int):
    if request.method == "GET":
        if Valtice_ucastnik.get_by_id(id) is None:
            flash("Uživatel s tímto ID neexistuje", category="error")
            return redirect(url_for("org_views.seznam_ucastniku"))
        return render_template("organizator/uprava_ucastnika.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("save"):
            u = Valtice_ucastnik.get_by_id(id)
            u.nacist_zmeny_z_requestu(request)
            flash("Změny byly uloženy", category="success")
            return redirect(url_for("org_views.ucastnik", id=id))
        elif request.form.get("zrusit_registraci"):
            u = Valtice_ucastnik.get_by_id(id)
            u.cas_registrace = None
            u.update()
            flash("Registrace byla zrušena", category="success")
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("registrovat_nyni"):
            u = Valtice_ucastnik.get_by_id(id)
            u.cas_registrace = datetime.now()
            u.update()
            flash("Uživatel byl zaregistrován", category="success")
            return redirect(url_for("org_views.uprava_ucastnika", id=id))
        elif request.form.get("zpet"):
            return redirect(url_for("org_views.ucastnik", id=id))
        elif request.form.get("delete"):
            Valtice_ucastnik.get_by_id(id).delete()
            flash("Uživatel byl smazán", category="success")
            return redirect(url_for("org_views.seznam_ucastniku"))
        return request.form.to_dict()
    
    
@org_views.route("/seznam_ucastniku", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def seznam_ucastniku():
    if request.method == "GET":
        return render_template("organizator/seznam_ucastniku.html", roles=get_roles(current_user))
    else:
        return request.form.to_dict()
    

@org_views.route("/trida/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def trida(id:int):
    if request.method == "GET":
        return render_template("organizator/trida.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("upravit"):
            return redirect(url_for("org_views.uprava_tridy", id=id))
        else:
            return request.form.to_dict()
        

@org_views.route("/uprava_tridy/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def uprava_tridy(id:int):
    if request.method == "GET":
        return render_template("organizator/uprava_tridy.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("save"):
            t = Valtice_trida.get_by_id(id)
            t.nacist_zmeny_z_requestu(request)
            flash("Změny byly uloženy", category="success")
            return redirect(url_for("org_views.trida", id=id))
        elif request.form.get("zpet"):
            return redirect(url_for("org_views.trida", id=id))
        elif request.form.get("delete"):
            t = Valtice_trida.get_by_id(id)
            t.delete()
            flash("Třída byla smazána", category="success")
            return redirect(url_for("org_views.tridy"))
        else:
            return request.form.to_dict()
    

@org_views.route("/ceny", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def ceny():
    if request.method == "GET":
        return render_template("organizator/ceny.html", roles=get_roles(current_user))
    else:
        if request.form.get("ulozit"):
            for cena in Cena.get_all():
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
        
@org_views.route("/tridy", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def tridy():
    if request.method == "GET":
        return render_template("organizator/tridy.html", roles=get_roles(current_user))
    else:
        if id := request.form.get("trida"):
            return redirect(url_for("org_views.trida", id=id))
        else:
            return request.form.to_dict()
        
       
@org_views.route("/seznamy", methods=["GET","POST"])
@require_role_system_name_on_current_user("organizator")
def seznamy():
    if request.method == "GET":
        return render_template("organizator/seznamy.html", roles=get_roles(current_user))
    else:
        if request.form.get("ucel") == "excel":
            print("jsem tu")
            result = json.loads(request.form.get("data"))
            bytes = Valtice_ucastnik.vytvorit_xlsx_seznam(result)
            return send_file(bytes, as_attachment=True, download_name="seznam.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            # return make_response(send_file(bytes, as_attachment=True, download_name="seznam.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        elif request.form.get("ucel") == "pdf":
            kriteria = json.loads(request.form.get("data"))
            data_pro_tabulku = Valtice_ucastnik.vytvorit_seznam(kriteria)
            return render_template("organizator/pdf_seznam.html", data = json.dumps(data_pro_tabulku))
        elif request.form.get("ucel") == "view":
            result = json.loads(request.form.get("result"))
            data_pro_tabulku = Valtice_ucastnik.vytvorit_seznam(result)
            return json.dumps(data_pro_tabulku)
        else:
            return request.form.to_dict()