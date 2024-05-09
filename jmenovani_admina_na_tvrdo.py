"""
Tímhle skriptem můžu jmenovat registrovanýho usera adminem na základě e-mailu.
"""

import json
from website import create_app, db
from website.models.user import User
from website.models.role import Role

email_na_jmenovani = input("Napiš email: zaregistrovaného usera: ")

app = create_app()
with app.app_context():
    user_na_jmenovani = User.get_by_email(email_na_jmenovani)
    if user_na_jmenovani is None:
        print("Zadaný email v db neexistuje, asi ho musíš nejdřív registrovat.")
    else:
        for role in Role.get_all():
            user_na_jmenovani.roles.append(role)
        db.session.add(user_na_jmenovani)
        db.session.commit()
        print("Success")
