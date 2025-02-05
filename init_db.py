# Tento skript připraví databázi při prvním spuštění.
# NENÍ ošetřený proti opakovanému spuštění.
from website import create_app, db
from website.models.user import User
from website.models.billing import Billing
from website.models.role import Role
from werkzeug.security import generate_password_hash


app = create_app()
with app.app_context():
    
    #role
    Role(system_name="tutor", display_name="Lektor").update()
    Role(system_name="organiser", display_name="Organizátor").update()
    Role(system_name="editor", display_name="Editor").update()
    Role(system_name="admin", display_name="Admin").update()
    
    # josef admin
    if User.get_by_email("josef.latj@gmail.com") is not None:
        print("Admin už je v db.")
    else:
        
        josef = User(email="josef.latj@gmail.com", password=generate_password_hash("un1queValtice", method="scrypt"))
        for role in Role.get_all():
            josef.roles.append(role)
        db.session.add(josef)
        db.session.commit()
        print("Success")
    
    # ceny
    Billing(type="kurzovne", display_name="Běžné kurzovné", system_name="kurzovne").update()
    Billing(type="kurzovne", display_name="Kuzovné pro členy SSH", system_name="kurzovne_ssh").update()
    Billing(type="kurzovne", display_name="Kurzovné pro studenty", system_name="kurzovne_student").update()
    Billing(type="kurzovne", display_name="Ansámblové třídy", system_name="ansambly").update()
    Billing(type="kurzovne", display_name="Pasivní účast", system_name="kurzovne_pasivni").update()
    Billing(type="kurzovne", display_name="Děti do 15 let", system_name="kurzovne_deti").update()
    
    Billing(type="ubytovani", display_name="Internát Vinařské školy", system_name="internat").update()
    Billing(type="ubytovani", display_name="Tělocvična", system_name="telocvicna").update()
    
    Billing(type="strava", display_name="Snídaně SŠ", system_name="snidane_ss").update()
    Billing(type="strava", display_name="Snídaně ZŠ", system_name="snidane_zs").update()
    Billing(type="strava", display_name="Oběd SŠ", system_name="obed_ss").update()
    Billing(type="strava", display_name="Oběd ZŠ", system_name="obed_zs").update()
    Billing(type="strava", display_name="Večeře SŠ", system_name="vecere_ss").update()
    Billing(type="strava", display_name="Večeře ZŠ", system_name="vecere_zs").update()
    
    Billing(type="sleva", display_name="Sleva na sourozence", system_name="sleva_sourozenec").update()
    Billing(type="sleva", display_name="Sleva partnerské ZUŠ", system_name="sleva_zus").update()
    
