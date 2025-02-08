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
		return render_template("auth/cz_login.html")
	else:
		email = request.form.get("email")
		password = request.form.get("password")
		if len(email) > 100:
			flash("Zadaný e-mail byl určitě přiliš dlouhý.", category="error")
			return redirect(url_for("auth_views.login"))
		if len(password) > 300:    
			flash("Zadané heslo bylo určitě příliš dlouhé.", category="error")
			return redirect(url_for("auth_views.login"))
		user = User.get_by_email(email=email)
		if user and check_password_hash(user.password, password):
			user.login()
			flash("úspěšné přihlášení", category="success")
			return redirect(url_for("guest_views.cz_dashboard"))
		else:
			flash("E-mail nebo heslo byly špatně", category="error")
			return redirect(url_for("auth_views.login"))


@auth_views.route("/en_login", methods=["GET","POST"])
def en_login():
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.en_dashboard"))
	if request.method == "GET":
		return render_template("auth/en_login.html")
	else:
		return request.form.to_dict()


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
                -flash("Hesla se neshodují.", category="error")
                return redirect(url_for("auth_views.register"))
            elif len(password) == 0 or len(email) == 0:
                flash("E-mail a heslo nesmí být prázdné.", category="error")
                return redirect(url_for("auth_views.register"))
            elif u:=User.get_by_email(email=email):
                flash("Uživatel s tímto e-mailem již existuje.", category="error")
                return redirect(url_for("auth_views.register"))
            else:
                u = User(email=email, password=generate_password_hash(password, method="scrypt"))
                mail_sender(mail_identifier="confirm_email", target=email, data=u.get_reset_token())
                u.update()
                u.login()
                return redirect(url_for("auth_views.confirm_mail"))
        else:
            email = request.form.get("email_child")
            password = request.form.get("password_child")
            confirm = request.form.get("confirm_child")
            parent = User.get_by_email(email=email_odpovedne)
            if password != confirm:
                flash("Hesla se neshodují.", category="error")
                return redirect(url_for("auth_views.register"))
            if u := User.get_by_email(email=email):
                flash("Uživatel s tímto e-mailem již existuje.", category="error")
                return redirect(url_for("auth_views.register"))
            if parent is None:
                flash("E-mail odpovědné osoby nebyl nalezen.", category="error")
                return redirect(url_for("auth_views.register"))
            u = User()
            u.parent = parent
            mail_sender(mail_identifier="nove_dite", target=email_odpovedne)
            if (all([email, password])):
                u.email = email
                u.password = generate_password_hash(password, method="scrypt")
                mail_sender(mail_identifier="confirm_email", target=email, data=u.get_reset_token())
                u.update()
                u.login()
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
		return request.form.to_dict()


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
        return render_template("auth/en_confirm_mail.html", email = current_user.email)
    else:
        return request.form.to_dict()


@auth_views.route("/confirm_email/<token>", methods=["GET"])
@login_required
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
@login_required
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
		return redirect(url_for("guest_views.home"))
	if request.method == "GET":
		return render_template("auth/auth_request_reset.html")
	else:
		email = request.form.get("email")
		if len(email) > 100:
			flash("Zadaný e-mail byl určitě moc dlouhý.", category="error")
			return redirect(url_for("auth_views.request_reset"))
		user = User.get_by_email(email=email)
		if user:
			mail_sender(mail_identifier="reset_password", target=email, data=user.get_reset_token())
		flash("Pokud existuje uživatel s tímto e-mailem, byl mu odeslán ověřovací e-mail.", category="info")
		return redirect(url_for("auth_views.login"))


@auth_views.route("/reset_password/<token>", methods=["GET","POST"])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.home"))
	user = User.verify_reset_token(token)
	if user is None:
		flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
		return redirect(url_for("auth_views.request_reset"))
	if request.method == "GET":
		return render_template("auth/auth_reset_password.html")
	else:
		user.password = generate_password_hash(request.form.get("password"), method="scrypt")
		user.update()
		flash("Heslo změněno, můžete se nyní přihlásit:", category="info")
		return redirect(url_for("auth_views.login"))



