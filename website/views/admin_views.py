from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models.user import User, get_roles
from website.models.role import Role
from website.logs import delete_app_logs
import json
from website.helpers.require_role import require_role_system_name_on_current_user

admin_views = Blueprint("admin_views",__name__)


@admin_views.route("/")
@admin_views.route("/dashboard")
@require_role_system_name_on_current_user("admin")
def admin_dashboard():
    return render_template("admin/admin_dashboard.html", roles=get_roles())


@admin_views.route("/logs_file", methods=["GET","POST"])
@require_role_system_name_on_current_user("admin")
def logs_file():
    if request.method == "GET":
        return render_template("admin/admin_logs_file.html", roles=get_roles())
    else:
        delete_app_logs()
        flash("Logy úspěšně smazány", category="success")
        return redirect(url_for("admin_views.admin_dashboard"))

@admin_views.route("/jmenovat_adminy", methods=["GET", "POST"])
@require_role_system_name_on_current_user("super_admin")
def jmenovat_adminy():
    if request.method == "GET":
        return render_template("admin/admin_jmenovat_adminy.html", roles=get_roles())
    else:
        id = int(request.form.get("result"))
        print(id)
        return redirect(url_for("admin_views.vybrat_role_adminovi", id=id))
    
@admin_views.route("/jmenovat_adminy/<int:id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("super_admin")
def vybrat_role_adminovi(id):
    user = User.get_by_id(id)
    if request.method == "GET":
        return render_template("admin/admin_vybrat_role_adminovi.html", user=user, roles=get_roles())
    else:
        if request.form.get("detail"):
            return redirect(url_for("admin_views.detail_usera", id=request.form.get("detail")))
        else:
            nove_role = json.loads(request.form.get("result"))
            nove_role_objekty = [Role.get_by_system_name(r) for r in nove_role]
            if user.roles == nove_role_objekty:
                pass
            else:
                user.roles = nove_role_objekty
                user.update()
            flash("Role byly upraveny.", category="success")
            return redirect(url_for("admin_views.jmenovat_adminy"))
        
    
@admin_views.route("/detail_usera/<int:id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user(["admin"])
def detail_usera(id):
    if request.method == "GET":
        if id in [u.id for u in User.get_all()]:
            return render_template("admin/admin_detail_uzivatele.html", roles=get_roles(), id=id)
        else:
            flash("Uživatel s tímhle ID neexistuje.", category="error")
            return redirect(url_for("admin_views.edit_users"))
    else:
        if request.form.get("smazat"):
            user_na_odstraneni = User.get_by_id(id)
            if "admin" in get_roles(user_na_odstraneni):
                flash("Nemůžeš odstranit admina.", category="error")
            else:
                user_na_odstraneni.delete()
                flash("User smazán", category="success")
            return redirect(url_for("admin_views.admin_dashboard"))
        else:
            return request.form.to_dict()