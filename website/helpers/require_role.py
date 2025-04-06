from flask import abort, redirect, url_for
from flask_login import current_user
from functools import wraps

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


def ensure_email_password_participant(language): # cz/en
    #chatgpt written
    """
    Decorator to ensure that the current user has a confirmed email
    and does not need to change their password upon login
    and paarticipate in this year.
    If they do not have an email at all, they are a kid and are free to go.
    """
    def what_should_i_name_this(original_function):
        @wraps(original_function)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                if language == "cz":
                    return redirect(url_for("auth_views.login"))
                else:
                    return redirect(url_for("auth_views.en_login"))
            
            if current_user.email is None:
                pass
            
            elif not current_user.confirmed_email:
                if language == "cz":
                    return redirect(url_for("auth_views.confirm_mail"))
                else:
                    return redirect(url_for("auth_views.en_confirm_mail"))
            
            elif current_user.must_change_password_upon_login:
                if language == "cz":
                    return redirect(url_for("auth_views.change_password"))
                else:
                    return redirect(url_for("auth_views.en_change_password"))
            elif not current_user.is_this_year_participant:
                if language == "cz":
                    return redirect(url_for("auth_views.this_year_participation"))
                else:
                    return redirect(url_for("auth_views.en_this_year_participation"))
            return original_function(*args, **kwargs)
        return wrapper
    return what_should_i_name_this