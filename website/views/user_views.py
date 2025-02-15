from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, logout_user
from website.helpers.get_roles import get_roles
from website.models.user import User
from website.helpers.require_role import ensure_email_password
from website.mail_handler import mail_sender
from website.helpers.settings_manager import get_class_signup_state


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
                flash("Nemáte právo na toto dítě", "error")
                return redirect(url_for("user_views.account"))
        else:
            return request.form.to_dict()
    
    
@user_views.route("/en_account", methods=["GET", "POST"])
@ensure_email_password("en")
def en_account():
    if request.method == "GET":
        return render_template("user/en_account.html", roles=get_roles(), is_locked = current_user.is_locked)
    else:
        if id := request.form.get("child_id"):
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                logout_user()
                child.login()
                return redirect(url_for("user_views.en_account"))
            else:
                flash("You don't have permission for this child", "error")
                return redirect(url_for("user_views.en_account"))
    
    
@user_views.route("/edit_account", methods=["GET", "POST"])
@ensure_email_password("cz")
def edit_account():
    if request.method == "GET":
        return render_template("user/cz_edit_account.html", roles=get_roles())
    else:
        if id := request.form.get("unlink_child_id"):
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                child.parent_id = None
                child.update()
                flash("Účet odpojen", "success")
                return redirect(url_for("user_views.edit_account"))
            else:
                flash("Nemáte právo na toto dítě", "error")
                return redirect(url_for("user_views.edit_account"))
        elif request.form.get("save"):
            if request.form.get("parent_email"):
                user = User.get_by_email(request.form.get("parent_email"))
                if user:
                    if user == current_user:
                        flash("Nemůžete být nadřazeným účtem sám sobě", "error")
                        return redirect(url_for("user_views.edit_account"))
                    else:
                        current_user.parent = user
                        current_user.update()
                        flash("Nadřazený účet přidán", "success")
                else:
                    flash("Uživatel s tímto e-mailem neexistuje", "error")
            if request.form.get("email") != current_user.email:
                email = request.form.get("email")
                if User.get_by_email(email):
                    flash("Uživatel s tímto e-mailem již existuje", "error")
                else:
                    mail_sender("confirm_email", email, current_user.get_reset_token())
                    current_user.email = email
                    current_user.confirmed_email = False
                    current_user.update()
                    flash("E-mail úspěšně změněn.", "success")
            current_user.nacist_zmeny_z_user_requestu(request)
            flash("Změny uloženy", "success")
            return redirect(url_for("user_views.account"))
        else:
            return request.form.to_dict()


@user_views.route("/en_edit_account", methods=["GET", "POST"])
@ensure_email_password("en")
def en_edit_account():
    if request.method == "GET":
        return render_template("user/en_edit_account.html", roles=get_roles(), is_locked=current_user.is_locked)
    else:
        if id := request.form.get("unlink_child_id"):
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                child.parent_id = None
                child.update()
                flash("Account unlinked", "success")
                return redirect(url_for("user_views.en_edit_account"))
            else:
                flash("You don't have permission for this child", "error")
                return redirect(url_for("user_views.en_edit_account"))
        elif request.form.get("save"):
            if request.form.get("parent_email"):
                user = User.get_by_email(request.form.get("parent_email"))
                if user:
                    if user == current_user:
                        flash("You can't be parent to yourself", "error")
                        return redirect(url_for("user_views.en_edit_account"))
                    else:
                        current_user.parent = user
                        current_user.update()
                        flash("Parent account added", "success")
                else:
                    flash("User with this email doesn't exist", "error")
            if request.form.get("email") != current_user.email:
                email = request.form.get("email")
                if User.get_by_email(email):
                    flash("User with this email already exists", "error")
                else:
                    mail_sender("en_confirm_email", email, current_user.get_reset_token())
                    current_user.email = email
                    current_user.confirmed_email = False
                    current_user.update()
                    flash("E-mail successfully changed.", "success")
            current_user.nacist_zmeny_z_user_requestu(request)
            flash("Changes saved", "success")
            return redirect(url_for("user_views.en_account"))
        else:
            return request.form.to_dict()
        

@user_views.route("/zapis_tridy", methods=["GET", "POST"])
@ensure_email_password("cz")
def zapis_tridy():
    if request.method == "GET":
        return render_template("user/cz_class_signup.html", roles=get_roles(), class_signup_state=get_class_signup_state())
    else:
        return request.form.to_dict()
