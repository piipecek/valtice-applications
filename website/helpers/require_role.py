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
