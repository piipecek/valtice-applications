from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, logout_user
from website.helpers.get_roles import get_roles
from website.models.user import User
from website.helpers.require_role import ensure_email_password


user_views = Blueprint("user_views",__name__)


@user_views.route("/account", methods=["GET", "POST"])
@ensure_email_password("cz")
def account():
    if request.method == "GET":
        return render_template("user/cz_account.html", roles=get_roles(), is_locked = current_user.is_locked)
    else:
        if id := request.form.get("child_id"):
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                logout_user()
                child.login()
                return redirect(url_for("user_views.account"))
            else:
                flash("Nemáte právo na toto dítě", "danger")
                return redirect(url_for("user_views.account"))
        else:
            return request.form.to_dict()
    
    
@user_views.route("/en_account", methods=["GET", "POST"])
@ensure_email_password("en")
def en_account():
    if request.method == "GET":
        return render_template("user/en_account.html", roles=get_roles(), is_locked = current_user.is_locked)
    else:
        return request.form.to_dict()
    
    
@user_views.route("/edit_account", methods=["GET", "POST"])
@ensure_email_password("cz")
def edit_account():
    if request.method == "GET":
        return render_template("user/cz_edit_account.html", roles=get_roles())
    else:
        return request.form.to_dict()


@user_views.route("/en_edit_account", methods=["GET", "POST"])
@ensure_email_password("en")
def en_edit_account():
    if request.method == "GET":
        return render_template("user/en_edit_account.html", roles=get_roles(), is_locked=current_user.is_locked)
    else:
        return request.form.to_dict()
