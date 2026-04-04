from flask import abort, redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from website.mail_handler import mail_sender

def require_role_system_name_on_current_user(role_system_name: str, user = current_user):
    """Můj pokus o napsání login_required decoratoru

    Args:
        role_system_name (str | list): tahle role se vyžaduje | jedna z rolí se vyžaduje
        user (_type_, optional): _description_. Defaults to current_user.
    """
    if type(role_system_name) == str:
        role_system_name = [role_system_name]
    def what_should_i_name_this(original_function):
        @wraps(original_function)
        def wrapper(*args, **kwargs):
            should_abort = False
            if current_user.is_authenticated:
                user_roles = [r.system_name for r in user.roles]
                for r_input in role_system_name:
                    if r_input in user_roles:
                        result = original_function(*args, **kwargs)
                        return result
                else:
                    should_abort = True
            if should_abort:
                abort(401)
            else:
                return redirect(url_for("auth_views.login"))
        return wrapper
    return what_should_i_name_this


def ensure_valid_participant(language): # cz/en
    #chatgpt written
    """
    Decorator to ensure that the current user has all the necessary data:
        - logged in. if not -> login page
        - if they do not have e-mail, skip the e-mail check, they are a kid.
        - if they do have e-mail, it must be confirmed. if not -> send confirmation e-mail and redirect to confirmation page
        - if they must change their password upon login, redirect to change password page
        - if they are not this year's participant, flash a message and let them go
        - if they don't have {name, surname, date_of_birth}, redirect them to page where this data must be filled in
    """
    def what_should_i_name_this(original_function):
        @wraps(original_function)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                if language == "cz":
                    return redirect(url_for("auth_views.login"))
                else:
                    return redirect(url_for("auth_views.en_login"))
            
            if current_user.email:
                if not current_user.confirmed_email:
                    if language == "cz":
                        mail_sender(mail_identifier="confirm_email", target=current_user.email, data=current_user.get_reset_token())
                        return redirect(url_for("auth_views.confirm_mail"))
                    else:
                        mail_sender(mail_identifier="en_confirm_email", target=current_user.email, data=current_user.get_reset_token())
                        return redirect(url_for("auth_views.en_confirm_mail"))
            
            if current_user.must_change_password_upon_login:
                if language == "cz":
                    return redirect(url_for("auth_views.change_password"))
                else:
                    return redirect(url_for("auth_views.en_change_password"))
            
            if not current_user.name or not current_user.surname or not current_user.date_of_birth:
                if language == "cz":
                    return redirect(url_for("user_views.required_data"))
                else:
                    return redirect(url_for("user_views.en_required_data"))
                
            if not current_user.is_this_year_participant:
                if language == "cz":
                    flash("Nejste letošním účastníkem. Pokud se chcete letos MLŠSH účastnit, proveďte tuto změnu na svém účtu.", category="error")
                else:
                    flash("You are not this year's participant. If you want to participate this year, please change it in your account.", category="error")
                    
            return original_function(*args, **kwargs)
        return wrapper
    return what_should_i_name_this