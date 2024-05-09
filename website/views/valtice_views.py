from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.valtice_ucastnik import Valtice_ucastnik
import csv
from io import StringIO

valtice_views = Blueprint("valtice_views",__name__)

@valtice_views.route("/", methods=["GET","POST"])
@require_role_system_name_on_current_user("valtice_org")
def home():
    if request.method == "GET":
        return render_template("valtice/dashboard.html")
    else:
        if request.form.get("trida_button"):
            return redirect(url_for("valtice_views.trida", id=request.form.get("id_tridy")))
        elif request.form.get("soubor"):
            if 'file' not in request.files:
                flash("Nebyl nahrán žádný soubor", category="error")
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash("Nebyl nahrán žádný soubor", category="error")
                return redirect(request.url)
            if file and file.filename.endswith('.csv'):
                text_stream = StringIO(file.stream.read().decode('utf-8'))
                csv_reader = csv.reader(text_stream, delimiter=',')
                rows = list(csv_reader)
                result = Valtice_ucastnik.vytvorit_nove_ucastniky_z_csv(rows)
                flash(f"Bylo úspěšně vytvořeno {result['new']} nových účastníků, přeskočeno bylo {result['skipped']} existujících.", category="success")
                return redirect(request.url)
            else:
                return 'Invalid file format'
        elif request.form.get("vsichni"):
            return redirect(url_for("valtice_views.seznam_ucastniku"))
        return request.form.to_dict()
    
    
@valtice_views.route("/ucastnik/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("valtice_org")
def ucastnik(id:int):
    if request.method == "GET":
        return render_template("valtice/ucastnik.html", id=id)
    else:
        if id:=request.form.get("smazat"):
            Valtice_ucastnik.get_by_id(id).delete()
            flash("Uživatel byl smazán", category="success")
            return redirect(url_for("valtice_views.seznam_ucastniku"))
        return request.form.to_dict()
    
    
@valtice_views.route("/seznam_ucastniku", methods=["GET","POST"])
@require_role_system_name_on_current_user("valtice_org")
def seznam_ucastniku():
    if request.method == "GET":
        return render_template("valtice/seznam_ucastniku.html")
    else:
        if id:=request.form.get("result"):
            return redirect(url_for("valtice_views.ucastnik", id=id))
        return request.form.to_dict()
    

@valtice_views.route("/trida/<int:id>", methods=["GET","POST"])
@require_role_system_name_on_current_user("valtice_org")
def trida(id:int):
    if request.method == "GET":
        return render_template("valtice/trida.html", id=id)
    else:
        return request.form.to_dict()