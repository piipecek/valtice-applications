from flask import Blueprint, render_template
from flask_login import current_user
from website.models.user import get_roles


guest_views = Blueprint("guest_views",__name__)


@guest_views.route("/")
@guest_views.route("/dashboard")
def dashboard():
    return render_template("guest/dashboard.html", roles=get_roles(current_user))