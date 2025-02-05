from website.models.user import User
from flask_login import current_user
from typing import List

def get_roles(u: "User" = current_user) -> List[str]:
    result = []
    if u.is_authenticated:
        result.append("prihlasen")
        result.extend([r.system_name for r in u.roles])
    return result