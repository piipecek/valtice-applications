from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from website.models.user import get_roles
from website.models.suggestion import Suggestion
from website.paths import multilang_path
import json


guest_views = Blueprint("guest_views",__name__)


@guest_views.route("/")
@guest_views.route("/dashboard")
def dashboard():
    return render_template("guest/dashboard.html", roles=get_roles(current_user))

@guest_views.route("/known_bugs")
def known_bugs():
    return render_template("guest/zname_chyby.html", roles=get_roles(current_user))

@guest_views.route("/historie")
def historie():
    return render_template("guest/historie_verzi.html", roles=get_roles(current_user))

@guest_views.route("/nahlasit_bug", methods=["GET","POST"])
def nahlasit_bug():
    if request.method == "GET":
        return render_template("guest/nahlasit_chybu.html", roles=get_roles(current_user))
    else:
        autor = None
        if current_user.is_authenticated:
            autor = current_user if request.form.get("include_name") else None
        s = Suggestion(value = request.form.get("popis"), author = autor)
        s.update()
        return redirect(url_for("guest_views.known_bugs"))

@guest_views.route("/planovane_featury")
def planovane_featury():
    return render_template("guest/planovane_featury.html", roles=get_roles(current_user))


@guest_views.route("send_multilang/<string:lang>/<string:location>")
def send_multilang(lang, location) -> str:
    with open(multilang_path()) as file:
        file = json.load(file)

    result = []
    for zaznam in file:
        if zaznam["location"] == location:
            novy_zaznam = {
                "name": zaznam["name"],
            }
            if lang in zaznam["translations"]:
                novy_zaznam["preklad"] = zaznam["translations"][lang]
            else:
                name = zaznam["name"]
                novy_zaznam["preklad"] = f"Tahle kombinace jména a lokace ({name}, {location}) nemá překald pro {lang}."
            result.append(novy_zaznam)

    return json.dumps(result)
