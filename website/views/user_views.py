from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, logout_user
from website.helpers.get_roles import get_roles
from website.models.user import User
from website.helpers.require_role import ensure_email_password_participant
from website.mail_handler import mail_sender
from datetime import datetime


user_views = Blueprint("user_views",__name__)


@user_views.route("/account", methods=["GET", "POST"])
@ensure_email_password_participant("cz")
def account():
    if request.method == "GET":
        return render_template("user/cz_account.html", roles=get_roles(), is_locked = current_user.is_locked)
    else:
        if request.form.get("send_calc"):
            if current_user.parent:
                target = current_user.parent.email
            else:
                target = current_user.email
            mail_sender(mail_identifier="send_calculation", target=target, data=current_user.info_for_calculation_email())
            current_user.datetime_calculation_email = datetime.now()
            current_user.update()
            flash("E-mail s platebními údaji byl odeslán", category="success")
            return redirect(url_for("user_views.account", id=id))
        else:
            return request.form.to_dict()


@user_views.route("/cz_child_account/<int:id>", methods=["GET", "POST"])
@ensure_email_password_participant("cz")
def child_account(id):
    child = User.get_by_id(id)
    if child and child.parent_id == current_user.id:
        pass
    else:
        flash("Nemáte právo na toto dítě", "error")
        return redirect(url_for("user_views.account"))
    if request.method == "GET":
        return render_template("user/cz_child_account.html", id = id, roles=get_roles())
    else:
        if id := request.form.get("child_id"):
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                session["parent_id"] = current_user.id
                logout_user()
                child.login()
                return redirect(url_for("user_views.account"))
            else:       
                flash("Nemáte právo na toto dítě", "error")
                return redirect(url_for("user_views.account"))
        else:
            return request.form.to_dict()       


@user_views.route("/return_to_parent", methods=["GET"])
def return_to_parent():
    parent_id = session.pop("parent_id", None)
    if parent_id:
        parent = User.get_by_id(parent_id)
        if parent:
            if current_user.parent == parent:
                logout_user()
                parent.login()
                return redirect(url_for("user_views.account"))
            else:
                flash("Nemáte právo se vrátit k tomuto rodiči", "error")
                return redirect(url_for("user_views.account"))
        else:
            flash("Rodič s tímto ID neexistuje, přihlaste se znovu.", "error")
            return redirect(url_for("user_views.account"))
    else:
        flash("Někde se ztratilo ID rodiče, přihlaste se znovu.", "error")
        return redirect(url_for("user_views.account"))
    
    
@user_views.route("/en_account", methods=["GET", "POST"])
@ensure_email_password_participant("en")
def en_account():
    if request.method == "GET":
        return render_template("user/en_account.html", roles=get_roles(), is_locked = current_user.is_locked)
    else:
        if id := request.form.get("child_id"):
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                session["parent_id"] = current_user.id
                logout_user()
                child.login()
                return redirect(url_for("user_views.en_account"))
            else:
                flash("You don't have permission for this child", "error")
                return redirect(url_for("user_views.en_account"))
        elif request.form.get("send_calc"):
            if current_user.parent:
                target = current_user.parent.email
            else:
                target = current_user.email
            mail_sender(mail_identifier="en_send_calculation", target=target, data=current_user.info_for_calculation_email())
            current_user.datetime_calculation_email = datetime.now()
            current_user.update()
            flash("E-mail with payment details was sent", category="success")
            return redirect(url_for("user_views.en_account", id=id))
        else:
            return request.form.to_dict()
        

@user_views.route("/en_child_account/<int:id>", methods=["GET", "POST"])
@ensure_email_password_participant("en")
def en_child_account(id):
    child = User.get_by_id(id)
    if child and child.parent_id == current_user.id:
        pass
    else:
        flash("You don't have permission for this child", "error")
        return redirect(url_for("user_views.en_account"))
    if request.method == "GET":
        return render_template("user/en_child_account.html", id = id, roles=get_roles())
    else:
        if id := request.form.get("child_id"):
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                session["parent_id"] = current_user.id
                logout_user()
                child.login()
                return redirect(url_for("user_views.en_account"))
            else:       
                flash("You don't have permission for this child", "error")
                return redirect(url_for("user_views.en_account"))
        else:
            return request.form.to_dict()  
        
        
@user_views.route("/en_return_to_parent", methods=["GET"])
def en_return_to_parent():
    parent_id = session.pop("parent_id", None)
    if parent_id:
        parent = User.get_by_id(parent_id)
        if parent:
            if current_user.parent == parent:
                logout_user()
                parent.login()
                return redirect(url_for("user_views.en_account"))
            else:
                flash("You don't have permission to return to this parent", "error")
                return redirect(url_for("user_views.en_account"))
        else:
            flash("Parent with this ID doesn't exist, please log in again.", "error")
            return redirect(url_for("user_views.en_account"))
    else:
        flash("Somewhere the parent's ID was lost, please log in again.", "error")
        return redirect(url_for("user_views.en_account"))
    
    
@user_views.route("/edit_account", methods=["GET", "POST"])
@ensure_email_password_participant("cz")
def edit_account():
    if request.method == "GET":
        return render_template("user/cz_edit_account.html", roles=get_roles())
    else:
        if request.form.get("save"):
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
            if request.form.get("email") in ["", None]:
                if current_user.parent:
                    pass
                else:
                    flash("E-mail je povinný, byl Vám ponechán e-mail beze změny", "info")
            elif request.form.get("email") != current_user.email:
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
@ensure_email_password_participant("en")
def en_edit_account():
    if request.method == "GET":
        return render_template("user/en_edit_account.html", roles=get_roles(), is_locked=current_user.is_locked)
    else:
        if request.form.get("save"):
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
            if request.form.get("email") in ["", None]:
                if current_user.parent:
                    pass
                else:
                    flash("E-mail is mandatory, your previous e-mail was not changed.", "info")
            elif request.form.get("email") != current_user.email:
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
        
        
@user_views.route("/edit_child_account/<int:id>", methods=["GET", "POST"])
@ensure_email_password_participant("cz")
def edit_child_account(id):
    child = User.get_by_id(id)
    if child and child.parent_id == current_user.id:
        pass
    else:
        flash("Nemáte právo na toto dítě", "error")
        return redirect(url_for("user_views.account"))
    
    if request.method == "GET":
        return render_template("user/cz_edit_child_account.html", roles=get_roles(), id=id)
    else:
        if request.form.get("unlink"):
            id = request.form.get("unlink_child_id")
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                if child.email and child.password:
                    child.parent_id = None
                    child.update()
                    flash("Účet odpojen", "success")
                else:
                    flash("Účet bez e-mailu a hesla nelze odpojit, protože by se k němu pak nikdo nedostal. Nejprve nastavte e-mail a heslo pro tento účet.", "error")
                return redirect(url_for("user_views.account"))
            else:
                flash("Nemáte právo na toto dítě", "error")
                return redirect(url_for("user_views.account"))
        elif delete_id := request.form.get("delete_child_id"):
            child = User.get_by_id(delete_id)
            if child and child.parent_id == current_user.id:
                child.delete()
                flash("Účet smazán", "success")
                return redirect(url_for("user_views.account"))
            else:
                flash("Nemáte právo na toto dítě", "error")
                return redirect(url_for("user_views.account"))
        elif request.form.get("save"):
            if request.form.get("new_manager_email"):
                user = User.get_by_email(request.form.get("new_manager_email"))
                if user:
                    if user == current_user:
                        flash("Nemůžete být nadřazeným účtem sám sobě", "error")
                        return redirect(url_for("user_views.edit_account"))
                    else:
                        child.parent = user
                        child.update()
                        flash("Nadřazený účet změněn", "success")
                        return redirect(url_for("user_views.account"))
                else:
                    flash("Uživatel s tímto e-mailem neexistuje", "error")
            if request.form.get("email") != child.email:
                # plati i pokud email neni zadanej -> proste rodic to muze prepsat jakkoli
                child.email = request.form.get("email")
                child.confirmed_email = False
                child.update()
            child.nacist_zmeny_z_user_requestu(request)
            flash("Změny uloženy", "success")
            return redirect(url_for("user_views.child_account", id=id))
        else:
            return request.form.to_dict()
        
        
@user_views.route("/en_edit_child_account/<int:id>", methods=["GET", "POST"])
@ensure_email_password_participant("en")
def en_edit_child_account(id):
    child = User.get_by_id(id)
    if child and child.parent_id == current_user.id:
        pass
    else:
        flash("You do not have permission for this child", "error")
        return redirect(url_for("user_views.en_account"))
    
    if request.method == "GET":
        return render_template("user/en_edit_child_account.html", roles=get_roles(), id=id)
    else:
        if request.form.get("unlink"):
            id = request.form.get("unlink_child_id")
            child = User.get_by_id(id)
            if child and child.parent_id == current_user.id:
                if child.email and child.password:
                    child.parent_id = None
                    child.update()
                    flash("Account unlinked", "success")
                else:
                    flash("Account without email and password cannot be unlinked, because no one would be able to access it later. First set email and password for this account.", "error")
                return redirect(url_for("user_views.en_account"))
            else:
                flash("You do not have permission for this child", "error")
                return redirect(url_for("user_views.en_account"))
        elif delete_id := request.form.get("delete_child_id"):
            child = User.get_by_id(delete_id)
            if child and child.parent_id == current_user.id:
                child.delete()
                flash("Account deleted", "success")
                return redirect(url_for("user_views.en_account"))
            else:
                flash("You do not have permission for this child", "error")
                return redirect(url_for("user_views.en_account"))
        elif request.form.get("save"):
            if request.form.get("new_manager_email"):
                user = User.get_by_email(request.form.get("new_manager_email"))
                if user:
                    if user == current_user:
                        flash("You cannot be the manager of your own account", "error")
                        return redirect(url_for("user_views.en_edit_account"))
                    else:
                        child.parent = user
                        child.update()
                        flash("Manager account changed", "success")
                        return redirect(url_for("user_views.en_account"))
                else:
                    flash("User with this email does not exist", "error")
            if request.form.get("email") != child.email:
                # plati i pokud email neni zadanej -> proste rodic to muze prepsat jakkoli
                child.email = request.form.get("email")
                child.confirmed_email = False
                child.update()
            child.nacist_zmeny_z_user_requestu(request)
            flash("Changes saved", "success")
            return redirect(url_for("user_views.en_child_account", id=id))
        else:
            return request.form.to_dict()
        
@user_views.route("/new_child", methods=["GET", "POST"])
@ensure_email_password_participant("cz")
def new_child():
    if request.method == "GET":
        return render_template("user/cz_new_child.html", roles=get_roles())
    else:
        if request.form.get("child_select") == "ano": # chce ucet s mailem a heslem. overit neexistenci mailu a poslat overovaci.
            email = request.form.get("email")
            if User.get_by_email(email):
                flash("Uživatel s tímto e-mailem již existuje", "error")
                return redirect(url_for("user_views.new_child"))
            else:
                u = User()
                u.name = request.form.get("name")
                u.surname = request.form.get("surname")
                u.email = email
                u.parent = current_user
                u.date_of_birth = datetime.strptime(request.form.get("date_of_birth"), "%Y-%m-%d") if request.form.get("date_of_birth") else None
                u.update()
                mail_sender("confirm_email", email, u.get_reset_token())
                flash("Účet dítěte vytvořen, e-mail s potvrzením odeslán na " + email, "success")
                return redirect(url_for("user_views.child_account", id=u.id))
        else: # chce ucet bez mailu a hesla
            u = User()
            u.name = request.form.get("name")
            u.surname = request.form.get("surname")
            u.parent = current_user
            u.date_of_birth = datetime.strptime(request.form.get("date_of_birth"), "%Y-%m-%d") if request.form.get("date_of_birth") else None
            u.update()
            flash("Účet dítěte vytvořen", "success")
            return redirect(url_for("user_views.child_account", id=u.id))
        

@user_views.route("/en_new_child", methods=["GET", "POST"])
@ensure_email_password_participant("en")
def en_new_child():
    if request.method == "GET":
        return render_template("user/en_new_child.html", roles=get_roles())
    else:
        if request.form.get("child_select") == "ano": # chce ucet s mailem a heslem. overit neexistenci mailu a poslat overovaci.
            email = request.form.get("email")
            if User.get_by_email(email):
                flash("User with this email already exists", "error")
                return redirect(url_for("user_views.en_new_child"))
            else:
                u = User()
                u.name = request.form.get("name")
                u.surname = request.form.get("surname")
                u.email = email
                u.parent = current_user
                u.date_of_birth = datetime.strptime(request.form.get("date_of_birth"), "%Y-%m-%d") if request.form.get("date_of_birth") else None
                u.update()
                mail_sender("confirm_email", email, u.get_reset_token())
                flash("Account created, verification email sent to " + email, "success")
                return redirect(url_for("user_views.en_child_account", id=u.id))
        else: # chce ucet bez mailu a hesla
            u = User()
            u.name = request.form.get("name")
            u.surname = request.form.get("surname")
            u.parent = current_user
            u.date_of_birth = datetime.strptime(request.form.get("date_of_birth"), "%Y-%m-%d") if request.form.get("date_of_birth") else None
            u.update()
            flash("Account created", "success")
            return redirect(url_for("user_views.en_child_account", id=u.id))


@user_views.route("/zapis_hlavni_tridy", methods=["GET", "POST"])
@ensure_email_password_participant("cz")
def zapis_hlavni_tridy():
    if not current_user.is_active_participant:
        flash("Pasivní účastníci se nemohou registrovat do tříd", "error")
        return redirect(url_for("user_views.account"))
    if request.method == "GET":
        return render_template("user/cz_main_class_signup.html", roles=get_roles())
    else:
        return request.form.to_dict()


@user_views.route("/zapis_vedlejsi_tridy", methods=["GET", "POST"])
@ensure_email_password_participant("cz")
def zapis_vedlejsi_tridy():
    if not current_user.is_active_participant:
        flash("Pasivní účastníci se nemohou registrovat do tříd", "error")
        return redirect(url_for("user_views.account"))
    if request.method == "GET":
        return render_template("user/cz_secondary_class_signup.html", roles=get_roles())
    else:
        return request.form.to_dict()

    
@user_views.route("/en_zapis_hlavni_tridy", methods=["GET", "POST"])
@ensure_email_password_participant("en")
def en_zapis_hlavni_tridy():
    if not current_user.is_active_participant:
        flash("Passive participants cannot register for classes", "error")
        return redirect(url_for("user_views.en_account"))
    if request.method == "GET":
        return render_template("user/en_main_class_signup.html", roles=get_roles())
    else:
        return request.form.to_dict()
    
    
@user_views.route("/en_zapis_vedlejsi_tridy", methods=["GET", "POST"])
@ensure_email_password_participant("en")
def en_zapis_vedlejsi_tridy():
    if not current_user.is_active_participant:
        flash("Passive participants cannot register for classes", "error")
        return redirect(url_for("user_views.en_account"))
    if request.method == "GET":
        return render_template("user/en_secondary_class_signup.html", roles=get_roles())
    else:
        return request.form.to_dict()
