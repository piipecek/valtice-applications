from flask import Blueprint, render_template, request
from flask_login import login_required
from website.helpers.get_roles import get_roles


user_views = Blueprint("user_views",__name__)


@user_views.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "GET":
        return render_template("user/cz_account.html", roles=get_roles())
    else:
        return request.form.to_dict()
    
@user_views.route("/en_account", methods=["GET", "POST"])
@login_required
def en_account():
    if request.method == "GET":
        return render_template("user/en_account.html", roles=get_roles())
    else:
        return request.form.to_dict()
