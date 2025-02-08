from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.helpers.get_roles import get_roles
from website.helpers.require_role import ensure_email_password


user_views = Blueprint("user_views",__name__)


@user_views.route("/account", methods=["GET", "POST"])
@ensure_email_password("cz")
def account():
    # if current_user.email and not current_user.confirmed_email:
    #     return redirect(url_for("auth_views.confirm_mail")) # tohle a zda musi zmenit heslo MUSim dat do decoratoru a pokud uzivatel nema e-mail, je to tedy dite a sem ho pustit muzem
    if request.method == "GET":
        return render_template("user/cz_account.html", roles=get_roles())
    else:
        return request.form.to_dict()
    
    
@user_views.route("/en_account", methods=["GET", "POST"])
@ensure_email_password("en")
def en_account():
    if current_user.email and not current_user.confirmed_email:
        return redirect(url_for("auth_views.en_confirm_mail"))
    if request.method == "GET":
        return render_template("user/en_account.html", roles=get_roles())
    else:
        return request.form.to_dict()
