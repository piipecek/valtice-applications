from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.helpers.require_role import require_role_system_name_on_current_user

valtice_views = Blueprint("valtice_views",__name__)

@valtice_views.route("/")
@require_role_system_name_on_current_user("valtice_org")
def home():
    if request.method == "GET":
        return render_template("valtice/dashboard.html")
    else:
        return request.form.to_dict()