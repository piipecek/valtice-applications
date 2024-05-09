from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from website.models.user import get_roles
from website.helpers.require_role import require_role_system_name_on_current_user
from website.mail_handler import mail_sender
from website.models.user import User


user_views = Blueprint("user_views",__name__)


@user_views.route("/ucet", methods=["GET","POST"])
@require_role_system_name_on_current_user("user")
def ucet():
    if request.method == "GET":
        return render_template("user/ucet.html", roles=get_roles(current_user), confirmed = current_user.confirmed)
    else:
        if request.form.get("confirmation_email"):
            mail_sender("potvrzeni_emailu", target=current_user.email, data=current_user.get_reset_token())
            flash("Ověřovací e-mail odeslán.", category="success")
            return redirect(url_for("user_views.ucet"))
        else:
            return request.form.to_dict()
             
             
@user_views.route("/ucet/<token>", methods=["GET"])
def ucet_overeny(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("Ověřovací link vypršel, nebo je jinak neplatný.", category="info")
        return redirect(url_for("user_views.ucet"))
    else:
        user.confirmed = True
        user.update()
        user.login()
        flash("E-mail máte nyní ověřený.", category="success")
        return redirect(url_for("user_views.ucet"))