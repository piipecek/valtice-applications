from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user
from website.mail_handler import mail_sender

auth_views = Blueprint("auth_views",__name__, template_folder="auth")

@auth_views.route("/login", methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.dashboard"))
	if request.method == "GET":
		return render_template("auth/auth_login.html")
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
			return redirect(url_for("guest_views.dashboard"))
		else:
			flash("E-mail nebo heslo byly špatně", category="error")
			return redirect(url_for("auth_views.login"))

@auth_views.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Odhlášení proběhlo úspěšně.", category="info")
	return redirect(url_for("guest_views.dashboard"))


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



