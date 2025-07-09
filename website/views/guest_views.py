from flask import Blueprint, render_template, flash
from flask_login import current_user
from website.helpers.get_roles import get_roles
import datetime

guest_views = Blueprint("guest_views",__name__)


@guest_views.route("/")
@guest_views.route("/dashboard")
def cz_dashboard():
    return render_template("guest/cz_dashboard.html", roles=get_roles(current_user))

@guest_views.route("/en/")
@guest_views.route("/en_dashboard")
def en_dashboard():
    return render_template("guest/en_dashboard.html", roles=get_roles(current_user))

@guest_views.route("/prihlaska")
def cz_prihlaska():
    return render_template("guest/cz_prihlaska.html", roles=get_roles(current_user))

@guest_views.route("/en_prihlaska")
def en_prihlaska():
    return render_template("guest/en_prihlaska.html", roles=get_roles(current_user))

@guest_views.route("/informace")
def cz_info():
    return render_template("guest/cz_info.html", roles=get_roles(current_user), year=datetime.datetime.now().year)

@guest_views.route("/en_informace")
def en_info():
    return render_template("guest/en_info.html", roles=get_roles(current_user), year=datetime.datetime.now().year)

