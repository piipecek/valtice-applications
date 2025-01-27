from flask import Blueprint, render_template
from flask_login import current_user
from website.models.user import get_roles
from website.helpers.settings_manager import get_faze_for_dashboard, get_datetime_zacatku_for_dashboard


guest_views = Blueprint("guest_views",__name__)


@guest_views.route("/")
@guest_views.route("/dashboard")
def dashboard():
    return render_template("guest/dashboard.html", roles=get_roles(current_user), faze = get_faze_for_dashboard(), datetime_zacatku = get_datetime_zacatku_for_dashboard() )

@guest_views.route("/prihlaska")
def prihlaska():
    return render_template("guest/prihlaska.html")