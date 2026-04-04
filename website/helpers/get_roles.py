from website.models.user import User
from flask_login import current_user
from typing import List

def get_roles(u: "User" = current_user) -> List[str]:
    if not u.is_authenticated:
        return []
    
    result = [r.system_name for r in u.roles]
    
    if current_user.is_authenticated and current_user.id == u.id:
        result.append("prihlasen")
    
    return result