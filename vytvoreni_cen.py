"""
Tímhle skriptem se vytvoří ceny.
"""

from website import create_app
from website.models.cena import Cena

app = create_app()
with app.app_context():
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
    print("done")