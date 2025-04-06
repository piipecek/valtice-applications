from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models.user import User
from website.helpers.get_roles import get_roles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user
from website.mail_handler import mail_sender


auth_views = Blueprint("auth_views",__name__, template_folder="auth")


@auth_views.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.cz_dashboard"))
    if request.method == "GET":
        return render_template("auth/cz_login.html", roles = get_roles())
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if not all([email, password]):
            flash("E-mail a heslo nesmí být prázdné.", category="error")
            return redirect(url_for("auth_views.login"))
        user = User.get_by_email(email=email)
        if user and check_password_hash(user.password, password):
            user.login()
            flash("úspěšné přihlášení", category="success")
            return redirect(url_for("user_views.account"))
        else:
            flash("E-mail nebo heslo byly špatně", category="error")
            return redirect(url_for("auth_views.login"))


@auth_views.route("/en_login", methods=["GET","POST"])
def en_login():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.en_dashboard"))
    if request.method == "GET":
        return render_template("auth/en_login.html", roles = get_roles())
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if not all([email, password]):
            flash("Email and password must not be empty.", category="error")
            return redirect(url_for("auth_views.en_login"))
        user = User.get_by_email(email=email)
        if user and check_password_hash(user.password, password):
            user.login()
            flash("Login successful", category="success")
            return redirect(url_for("user_views.en_account"))
        else:
            flash("Email or password incorrect", category="error")
            return redirect(url_for("auth_views.en_login"))
		


@auth_views.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.cz_dashboard"))
    if request.method == "GET":
        return render_template("auth/cz_register.html", roles = get_roles())
    else:
        email_odpovedne = request.form.get("email_odpovedne")
        if email_odpovedne == "":
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            if password != confirm:
                flash("Hesla se neshodují.", category="error")
                return redirect(url_for("auth_views.register"))
            elif len(password) == 0 or len(email) == 0:
                flash("E-mail a heslo nesmí být prázdné.", category="error")
                return redirect(url_for("auth_views.register"))
            elif u:=User.get_by_email(email=email):
                flash("Uživatel s tímto e-mailem již existuje.", category="error")
                return redirect(url_for("auth_views.register"))
            else:
                u = User(email=email, password=generate_password_hash(password, method="scrypt"))
                u.update()
                u.login()
                mail_sender(mail_identifier="confirm_email", target=current_user.email, data=current_user.get_reset_token())
                return redirect(url_for("auth_views.confirm_mail"))
        else:
            email = request.form.get("email_child")
            password = request.form.get("password_child")
            confirm = request.form.get("confirm_child")
            parent = User.get_by_email(email=email_odpovedne)
            if password != confirm:
                flash("Hesla se neshodují.", category="error")
                return redirect(url_for("auth_views.register"))
            if u := User.get_by_email(email=email) and email != "":
                flash("Uživatel s tímto e-mailem již existuje.", category="error")
                return redirect(url_for("auth_views.register"))
            if parent is None:
                flash("E-mail odpovědné osoby nebyl nalezen.", category="error")
                return redirect(url_for("auth_views.register"))
            u = User()
            u.parent = parent
            mail_sender(mail_identifier="cz_new_child", target=email_odpovedne)
            u.update()
            u.login()
            if (all([email, password])):
                u.email = email
                u.password = generate_password_hash(password, method="scrypt")
                u.update()
                mail_sender(mail_identifier="confirm_email", target=current_user.email, data=current_user.get_reset_token())
                return redirect(url_for("auth_views.confirm_mail"))
            else:
                return redirect(url_for("user_views.account"))

@auth_views.route("/en_register", methods=["GET","POST"])
def en_register():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.en_dashboard"))
    if request.method == "GET":
        return render_template("auth/en_register.html", roles = get_roles())
    else:
        #the form names are same as in the czech version, so the same code can be used
        email_odpovedne = request.form.get("email_odpovedne")
        if email_odpovedne == "":
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            if password != confirm:
                -flash("Passwords do not match.", category="error")
                return redirect(url_for("auth_views.en_register"))
            elif len(password) == 0 or len(email) == 0:
                flash("Email and password must not be empty.", category="error")
                return redirect(url_for("auth_views.en_register"))
            elif u:=User.get_by_email(email=email):
                flash("User with this email already exists.", category="error")
                return redirect(url_for("auth_views.en_register"))
            else:
                u = User(email=email, password=generate_password_hash(password, method="scrypt"))
                u.update()
                u.login()
                mail_sender(mail_identifier="en_confirm_email", target=current_user.email, data=current_user.get_reset_token())
                return redirect(url_for("auth_views.en_confirm_mail"))
        else:
            email = request.form.get("email_child")
            password = request.form.get("password_child")
            confirm = request.form.get("confirm_child")
            parent = User.get_by_email(email=email_odpovedne)
            if password != confirm:
                flash("Passwords do not match.", category="error")
                return redirect(url_for("auth_views.en_register"))
            if u := User.get_by_email(email=email) and email != "":
                flash("User with this email already exists.", category="error")
                return redirect(url_for("auth_views.en_register"))
            if parent is None:
                flash("Email of the responsible person was not found.", category="error")
                return redirect(url_for("auth_views.en_register"))
            u = User()
            u.parent = parent
            mail_sender(mail_identifier="en_new_child", target=email_odpovedne)
            u.update()
            u.login()
            if (all([email, password])):
                u.email = email
                u.password = generate_password_hash(password, method="scrypt")
                u.update()
                mail_sender(mail_identifier="en_confirm_email", target=current_user.email, data=current_user.get_reset_token())
                return redirect(url_for("auth_views.en_confirm_mail"))
            else:
                return redirect(url_for("user_views.en_account"))


@auth_views.route("/confirm_mail", methods=["GET", "POST"])
@login_required
def confirm_mail():
    if current_user.confirmed_email:
        return redirect(url_for("user_views.account"))
    if request.method == "GET":
        return render_template("auth/cz_confirm_mail.html", email = current_user.email, roles = get_roles())
    else:
        if request.form.get("again"):
            mail_sender(mail_identifier="confirm_email", target=current_user.email, data=current_user.get_reset_token())
            flash("Ověřovací e-mail byl znovu odeslán.", category="info")
            return redirect(url_for("auth_views.confirm_mail"))
        else:
            return request.form.to_dict()
        

@auth_views.route("/en_confirm_mail", methods=["GET", "POST"])
@login_required
def en_confirm_mail():
    if current_user.confirmed_email:
        return redirect(url_for("user_views.en_account"))
    if request.method == "GET":
        return render_template("auth/en_confirm_mail.html", email = current_user.email, roles = get_roles())
    else:
        if request.form.get("again"):
            mail_sender(mail_identifier="en_confirm_email", target=current_user.email, data=current_user.get_reset_token())
            flash("Verification email has been sent again.", category="info")
            return redirect(url_for("auth_views.en_confirm_mail"))
        else:
            return request.form.to_dict()


@auth_views.route("/confirm_email/<token>", methods=["GET"])
def confirm_email(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("Ověřovací link vypršel, zkuste ověřit e-mail znovu.", category="info")
        return redirect(url_for("auth_views.confirm_mail"))
    else:
        user.confirmed_email = True
        user.update()
        flash("E-mail byl úspěšně ověřen.", category="success")
        return redirect(url_for("user_views.account"))


@auth_views.route("/en_confirm_email/<token>", methods=["GET"])
def en_confirm_email(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("Verification link expired, please verify email again.", category="info")
        return redirect(url_for("auth_views.en_confirm_mail"))
    else:
        user.confirmed_email = True
        user.update()
        flash("Email successfully verified.", category="success")
        return redirect(url_for("user_views.en_account"))
    

@auth_views.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Odhlášení proběhlo úspěšně.", category="info")
	return redirect(url_for("guest_views.cz_dashboard"))


@auth_views.route("/en_logout")
@login_required
def en_logout():
	logout_user()
	flash("Log out successful.", category="info")
	return redirect(url_for("guest_views.en_dashboard"))


@auth_views.route("/reset_password", methods=["GET","POST"])
def request_reset():
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.cz_dashboard"))
	if request.method == "GET":
		return render_template("auth/cz_request_reset.html")
	else:
		email = request.form.get("email")
		user = User.get_by_email(email=email)
		if user:
			mail_sender(mail_identifier="reset_password", target=email, data=user.get_reset_token())
		flash("Pokud existuje uživatel s tímto e-mailem, byl mu odeslán ověřovací e-mail.", category="info")
		return redirect(url_for("auth_views.login"))


@auth_views.route("/reset_password/<token>", methods=["GET","POST"])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.cz_dashboard"))
	user = User.verify_reset_token(token)
	if user is None:
		flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
		return redirect(url_for("auth_views.request_reset"))
	if request.method == "GET":
		return render_template("auth/cz_reset_password.html")
	else:
		user.password = generate_password_hash(request.form.get("password"), method="scrypt")
		user.update()
		flash("Heslo změněno, můžete se nyní přihlásit:", category="info")
		return redirect(url_for("auth_views.login"))


@auth_views.route("/en_reset_password", methods=["GET","POST"])
def en_request_reset():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.en_dashboard"))
    if request.method == "GET":
        return render_template("auth/en_request_reset.html")
    else:
        email = request.form.get("email")
        user = User.get_by_email(email=email)
        if user:
            mail_sender(mail_identifier="en_reset_password", target=email, data=user.get_reset_token())
        flash("If a user with this email exists, a verification email has been sent to them.", category="info")
        return redirect(url_for("auth_views.en_login"))


@auth_views.route("/en_reset_password/<token>", methods=["GET","POST"])
def en_reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.en_dashboard"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Reset link expired or is otherwise invalid.", category="info")
        return redirect(url_for("auth_views.en_request_reset"))
    if request.method == "GET":
        return render_template("auth/en_reset_password.html")
    else:
        user.password = generate_password_hash(request.form.get("password"), method="scrypt")
        user.update()
        flash("Password changed, you can now log in:", category="info")
        return redirect(url_for("auth_views.en_login"))


@auth_views.route("/change_password", methods=["GET","POST"])
@login_required
def change_password():
    if not current_user.must_change_password_upon_login:
        return redirect(url_for("user_views.account"))
    if request.method == "GET":
        return render_template("auth/cz_change_password.html", roles = get_roles())
    else:
        if request.form.get("keep"):
            current_user.must_change_password_upon_login = False
            current_user.update()
            return redirect(url_for("user_views.account"))
        elif request.form.get("change"):
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            if password != confirm:
                flash("Hesla se neshodují.", category="error")
                return redirect(url_for("auth_views.change_password"))
            elif len(password) == 0:
                flash("Heslo nesmí být prázdné.", category="error")
                return redirect(url_for("auth_views.change_password"))
            else:
                current_user.password = generate_password_hash(password, method="scrypt")
                current_user.must_change_password_upon_login = False
                current_user.update()
                flash("Heslo bylo úspěšně změněno.", category="success")
                return redirect(url_for("user_views.account"))
        else:
            return request.form.to_dict()
    

@auth_views.route("/en_change_password", methods=["GET","POST"])
@login_required
def en_change_password():
    if not current_user.must_change_password_upon_login:
        return redirect(url_for("user_views.en_account"))
    if request.method == "GET":
        return render_template("auth/en_change_password.html", roles = get_roles())
    else:
        if request.form.get("keep"):
            current_user.must_change_password_upon_login = False
            current_user.update()
            return redirect(url_for("user_views.en_account"))
        elif request.form.get("change"):
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            if password != confirm:
                flash("Passwords do not match.", category="error")
                return redirect(url_for("auth_views.en_change_password"))
            elif len(password) == 0:
                flash("Password must not be empty.", category="error")
                return redirect(url_for("auth_views.en_change_password"))
            else:
                current_user.password = generate_password_hash(password, method="scrypt")
                current_user.must_change_password_upon_login = False
                current_user.update()
                flash("Password successfully changed.", category="success")
                return redirect(url_for("user_views.en_account"))
        else:
            return request.form.to_dict()


@auth_views.route("/this_year_participation", methods=["GET", "POST"])
@login_required
def this_year_participation():
    if current_user.is_this_year_participant:
        return redirect(url_for("guest_views.cz_dashboard"))
    if request.method == "GET":
        return render_template("auth/cz_this_year_participation.html", roles=get_roles())
    else:
        if status := request.form.get("participates"):
            if status == "yes":
                current_user.is_this_year_participant = True
                current_user.update()
                flash("Zájem na tomto ročníku byl zaznamenán, děkujeme.", category="success")
                return redirect(url_for("user_views.account"))
            elif status == "no":
                flash("Váš účet stále bude existovat, ale bez zájmu o letošní ročník Vás dál nemůžeme pustit.", category="info")
                return redirect(url_for("auth_views.this_year_participation"))
        else:
            return request.form.to_dict()
        
    
@auth_views.route("/en_this_year_participation", methods=["GET", "POST"])
@login_required
def en_this_year_participation():
    if current_user.is_this_year_participant:
        return redirect(url_for("guest_views.en_dashboard"))
    if request.method == "GET":
        return render_template("auth/en_this_year_participation.html", roles=get_roles())
    else:
        if status := request.form.get("participates"):
            if status == "yes":
                current_user.is_this_year_participant = True
                current_user.update()
                flash("We noted your interest in this year's ISSEM, thank you.", category="success")
                return redirect(url_for("user_views.en_account"))
            elif status == "no":
                flash("Your account will still exist, but without interest in this year's ISSEM we cannot let you in.", category="info")
                return redirect(url_for("auth_views.en_this_year_participation"))
        else:
            return request.form.to_dict()