"""
Tímhle skriptem se vytvoří potřebný role pro běh:
Potom se dá skriptem "jmenovani_admina_na_tvrdo.py" pokračovat se všim z admin prostředí spuštěný aplikace.
"""

from website import create_app
from website.models.role import Role

app = create_app()
with app.app_context():
    Role(system_name="user", display_name="Uživatel").update()
    Role(system_name="admin", display_name="Admin").update()
    Role(system_name="editing_admins", display_name="Editování pravomocí adminů").update()
    Role(system_name="editing_roles", display_name="Úprava rolí").update()
    Role(system_name="editing_users", display_name="Úprava uživatelů").update()
    Role(system_name="editing_app_logs", display_name="Úprava app logů").update()
    Role(system_name="editing_admin_logs", display_name="Úprava admin logů").update()
    Role(system_name="editing_suggestions", display_name="Úprava připomínek").update()
    Role(system_name="editing_downtime", display_name="Úprava downtime").update()
    print("done")
