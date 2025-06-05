from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from website.models.user import User
from website.helpers.get_roles import get_roles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user
from website.mail_handler import mail_sender
import requests


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
            if user.is_this_year_participant:
                return redirect(url_for("user_views.account"))
            else:
                return redirect(url_for("auth_views.this_year_participation"))
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
            if user.is_this_year_participant:
                return redirect(url_for("user_views.en_account"))
            else:
                return redirect(url_for("auth_views.en_this_year_participation"))
        else:
            flash("Email or password incorrect", category="error")
            return redirect(url_for("auth_views.en_login"))
            

@auth_views.route("/register_intro", methods=["GET"])
def register_intro():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.cz_dashboard"))
    if request.method == "GET":
        return render_template("auth/cz_register_intro.html", roles = get_roles())
    else:
        return request.form.to_dict()


@auth_views.route("/register_adult", methods=["GET", "POST"])
def register_adult():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.cz_dashboard"))
    if request.method == "GET":
        return render_template("auth/cz_register_adult.html", roles=get_roles())
    else:
        recaptcha_response = request.form.get('g-recaptcha-response')
        secret = "6LdwoVYrAAAAAOmG5LgeSyCZTzKlm4C9RMXlYPGI"
        payload = {
            'secret': secret,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = r.json()
        
        if not result.get('success'):
            return "reCAPTCHA ověření selhalo. Zkuste to prosím znovu."
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password != confirm:
            flash("Hesla se neshodují.", category="error")
            return redirect(url_for("auth_views.register_adult"))
        elif len(password) == 0 or len(email) == 0:
            flash("E-mail a heslo nesmí být prázdné.", category="error")
            return redirect(url_for("auth_views.register_adult"))
        elif User.get_by_email(email=email):
            flash("Uživatel s tímto e-mailem již existuje.", category="error")
            return redirect(url_for("auth_views.register_adult"))
        else:
            user = User(email=email, password=generate_password_hash(password, method="scrypt"))
            user.update()
            user.login()
            mail_sender(mail_identifier="confirm_email", target=user.email, data=user.get_reset_token())
            flash("Registrace byla úspěšná. Ověřte prosím svůj e-mail.", category="success")
            return redirect(url_for("auth_views.confirm_mail"))
        

@auth_views.route("/register_child", methods=["GET", "POST"])
def register_child():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.cz_dashboard"))
    if request.method == "GET":
        return render_template("auth/cz_register_child.html", roles=get_roles())
    else:
        recaptcha_response = request.form.get('g-recaptcha-response')
        secret = "6LdwoVYrAAAAAOmG5LgeSyCZTzKlm4C9RMXlYPGI"
        payload = {
            'secret': secret,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = r.json()
        
        if not result.get('success'):
            return "reCAPTCHA ověření selhalo. Zkuste to prosím znovu."
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        should_have_email_password = True if request.form.get("child_select") == "ano" else False
        parent_email = request.form.get("email_odpovedne")
        parent = User.get_by_email(email=parent_email)
        if parent is None:
            flash("E-mail odpovědné osoby nebyl nalezen.", category="error")
            return redirect(url_for("auth_views.register_child"))
        if parent.is_under_16:
            flash("Odpovědná osoba musí být starší 16 let.", category="error")
            return redirect(url_for("auth_views.register_child"))
        if parent.parent:
            flash("Odpovědná osoba je sama připojena jako dítě.", category="error")
            return redirect(url_for("auth_views.register_child"))
        
        if not should_have_email_password:
            user = User()
            user.parent = parent
            mail_sender(mail_identifier="cz_new_child", target=parent_email)
            user.is_under_16 = True
            user.update()
            user.login()
            flash("Registrace byla úspěšná. Můžete pokračovat vyplňováním osobních údajů.", category="success")
            return redirect(url_for("user_views.account"))
        else:
            if password != confirm:
                flash("Hesla se neshodují.", category="error")
                return redirect(url_for("auth_views.register_child"))
            if len(password) == 0 or len(email) == 0:
                flash("Pokud chcete mít e-mail a heslo, nesmí být prázdné.", category="error")
                return redirect(url_for("auth_views.register_child"))
            if User.get_by_email(email=email):
                flash("Uživatel s tímto e-mailem již existuje.", category="error")
                return redirect(url_for("auth_views.register_child"))
        
            user = User()
            user.parent = parent
            user.is_under_16 = True
            user.email = email
            user.password = generate_password_hash(password, method="scrypt")
            user.update()
            mail_sender(mail_identifier="cz_new_child", target=parent_email)
            mail_sender(mail_identifier="confirm_email", target=user.email, data=user.get_reset_token())
            user.login()
            flash("Registrace byla úspěšná. Ověřte prosím svůj e-mail.", category="success")
            return redirect(url_for("auth_views.confirm_mail"))



@auth_views.route("/en_register_intro", methods=["GET"])
def en_register_intro():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.en_dashboard"))
    if request.method == "GET":
        return render_template("auth/en_register_intro.html", roles = get_roles())
    else:
        return request.form.to_dict()
    
    
@auth_views.route("/en_register_adult", methods=["GET", "POST"])
def en_register_adult():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.en_dashboard"))
    if request.method == "GET":
        return render_template("auth/en_register_adult.html", roles=get_roles())
    else:
        recaptcha_response = request.form.get('g-recaptcha-response')
        secret = "6LdwoVYrAAAAAOmG5LgeSyCZTzKlm4C9RMXlYPGI"
        payload = {
            'secret': secret,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = r.json()
        
        if not result.get('success'):
            return "reCAPTCHA ověření selhalo. Zkuste to prosím znovu."
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password != confirm:
            flash("Passwords do not match.", category="error")
            return redirect(url_for("auth_views.en_register_adult"))
        elif len(password) == 0 or len(email) == 0:
            flash("E-mail and password must not be empty.", category="error")
            return redirect(url_for("auth_views.en_register_adult"))
        elif User.get_by_email(email=email):
            flash("User with this e-mail already exists.", category="error")
            return redirect(url_for("auth_views.en_register_adult"))
        else:
            user = User(email=email, password=generate_password_hash(password, method="scrypt"))
            user.update()
            user.login()
            mail_sender(mail_identifier="en_confirm_email", target=user.email, data=user.get_reset_token())
            flash("Registration was successful. Please verify your e-mail.", category="success")
            return redirect(url_for("auth_views.en_confirm_mail"))
        
        
@auth_views.route("/en_register_child", methods=["GET", "POST"])
def en_register_child():
    if current_user.is_authenticated:
        return redirect(url_for("guest_views.en_dashboard"))
    if request.method == "GET":
        return render_template("auth/en_register_child.html", roles=get_roles())
    else:
        recaptcha_response = request.form.get('g-recaptcha-response')
        secret = "6LdwoVYrAAAAAOmG5LgeSyCZTzKlm4C9RMXlYPGI"
        payload = {
            'secret': secret,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = r.json()
        
        if not result.get('success'):
            return "reCAPTCHA ověření selhalo. Zkuste to prosím znovu."
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        should_have_email_password = True if request.form.get("child_select") == "ano" else False
        parent_email = request.form.get("email_odpovedne")
        parent = User.get_by_email(email=parent_email)
        if parent is None:
            flash("Responsible person's e-mail not found.", category="error")
            return redirect(url_for("auth_views.en_register_child"))
        if parent.is_under_16:
            flash("Responsible person must be older than 16 years.", category="error")
            return redirect(url_for("auth_views.en_register_child"))
        if parent.parent:
            flash("Responsible person is connected as a child themselves.", category="error")
            return redirect(url_for("auth_views.en_register_child"))
        
        if not should_have_email_password:
            user = User()
            user.parent = parent
            mail_sender(mail_identifier="en_new_child", target=parent_email)
            user.is_under_16 = True
            user.update()
            user.login()
            flash("Registration was successful. You can continue filling in personal details.", category="success")
            return redirect(url_for("user_views.en_account"))
        else:
            if password != confirm:
                flash("Passwords do not match.", category="error")
                return redirect(url_for("auth_views.en_register_child"))
            if len(password) == 0 or len(email) == 0:
                flash("If you want to have an e-mail and password, they must not be empty.", category="error")
                return redirect(url_for("auth_views.en_register_child"))
            if User.get_by_email(email=email):
                flash("User with this e-mail already exists.", category="error")
                return redirect(url_for("auth_views.en_register_child"))
        
            user = User()
            user.parent = parent
            user.is_under_16 = True
            user.email = email
            user.password = generate_password_hash(password, method="scrypt")
            user.update()
            mail_sender(mail_identifier="en_new_child", target=parent_email)
            mail_sender(mail_identifier="en_confirm_email", target=user.email, data=user.get_reset_token())
            user.login()
            flash("Registration was successful. Please verify your e-mail.", category="success")
            return redirect(url_for("auth_views.en_confirm_mail"))


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
        flash("E-mail successfully verified.", category="success")
        return redirect(url_for("user_views.en_account"))
    

@auth_views.route("/logout")
@login_required
def logout():
    session.clear() # musí být před logout_user()
    logout_user()
    flash("Odhlášení proběhlo úspěšně.", category="info")
    return redirect(url_for("guest_views.cz_dashboard"))


@auth_views.route("/en_logout")
@login_required
def en_logout():
    session.clear()
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
                return redirect(url_for("user_views.account"))
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
                return redirect(url_for("user_views.en_account"))
        else:
            return request.form.to_dict()