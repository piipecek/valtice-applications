# Tento skript připraví databázi při prvním spuštění.
# je ošetřený proti opakovanému spuštění.
from website import create_app, db
from website.models.user import User
from website.models.cena import Cena
from website.models.role import Role
from werkzeug.security import generate_password_hash


app = create_app()
with app.app_context():
    # josef admin
    if User.get_by_email("josef.latj@gmail.com") is not None:
        print("Admin už je v db.")
    else:
        
        josef = User(email="josef.latj@gmail.com", password=generate_password_hash("un1queValtice", method="sha256"))
        for role in Role.get_all():
            josef.roles.append(role)
        db.session.add(josef)
        db.session.commit()
        print("Success")
    
    # ceny
    Cena(typ="kurzovne", display_name="Běžné kurzovné", system_name="kurzovne").update()
    Cena(typ="kurzovne", display_name="Kuzovné pro členy SSH", system_name="kurzovne_ssh").update()
    Cena(typ="kurzovne", display_name="Kurzovné pro studenty", system_name="kurzovne_student").update()
    Cena(typ="kurzovne", display_name="Ansámblové třídy", system_name="ansambly").update()
    Cena(typ="kurzovne", display_name="Pasivní účast", system_name="kurzovne_pasivni").update()
    Cena(typ="kurzovne", display_name="Děti do 15 let", system_name="kurzovne_deti").update()
    
    Cena(typ="ubytovani", display_name="Internát Vinařské školy", system_name="internat").update()
    Cena(typ="ubytovani", display_name="Tělocvična", system_name="telocvicna").update()
    Cena(typ="strava", display_name="Snídaně SŠ", system_name="snidane_ss").update()
    Cena(typ="strava", display_name="Snídaně ZŠ", system_name="snidane_zs").update()
    Cena(typ="strava", display_name="Oběd SŠ", system_name="obed_ss").update()
    Cena(typ="strava", display_name="Oběd ZŠ", system_name="obed_zs").update()
    Cena(typ="strava", display_name="Večeře SŠ", system_name="vecere_ss").update()
    Cena(typ="strava", display_name="Večeře ZŠ", system_name="vecere_zs").update()
    
    #role
    Role(system_name="organizator", display_name="Organizátor").update()
    Role(system_name="admin", display_name="Admin").update()
    Role(system_name="super_admin", display_name="Super admin").update()
