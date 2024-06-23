"""
Tímhle skriptem se vytvoří třídy.
"""

from website import create_app
from website.models.cena import Cena

app = create_app()
with app.app_context():
    Cena(typ="kurzovne", display_name="Běžné kurzovné", system_name="kurzovne").update()
    Cena(typ="kurzovne", display_name="Běžné kurzovné - 2. třída", system_name="kurzovne_2").update()
    Cena(typ="kurzovne", display_name="Běžné kurzovné - komorní a ansámblové třídy", system_name="kurzovne_ansambly").update()
    Cena(typ="kurzovne", display_name="Pasivní účast", system_name="kurzovne_pasivni").update()
    Cena(typ="kurzovne", display_name="Kurzovné pro členy SSH", system_name="kurzovne_ssh").update()
    Cena(typ="kurzovne", display_name="Kurzovné pro členy SSH - 2. třída", system_name="kurzovne_ssh_2").update()
    Cena(typ="kurzovne", display_name="kurzovné pro členy SSH - komorní a ansámblové třídy ", system_name="kurzovne_ansambly_ssh").update()
    Cena(typ="kurzovne", display_name="Pasivní účast pro členy SSH", system_name="kurzovne_pasivni_ssh").update()
    Cena(typ="kurzovne", display_name="Kurzovné pro studenty", system_name="kurzovne_student").update()
    Cena(typ="kurzovne", display_name="Kurzovné pro studenty - 2. třída", system_name="kurzovne_student_2").update()
    Cena(typ="kurzovne", display_name="Kurzovné pro studenty - komorní a ansámblové třídy", system_name="kurzovne_ansambly_student").update()
    Cena(typ="kurzovne", display_name="Pasivní účast pro studenty", system_name="kurzovne_pasivni_student").update()
    Cena(typ="kurzovne", display_name="Děti do 15 let", system_name="kurzovne_deti").update()
    Cena(typ="ubytovaní", display_name="Internát Vinařské školy", system_name="internat").update()
    Cena(typ="ubytovaní", display_name="Tělocvična", system_name="telocvicna").update()
    Cena(typ="strava", display_name="Snídaně VŠ", system_name="snidane_vs").update()
    Cena(typ="strava", display_name="Snídaně ZŠ", system_name="snidane_zs").update()
    Cena(typ="strava", display_name="Oběd VŠ", system_name="obed_vs").update()
    Cena(typ="strava", display_name="Oběd ZŠ", system_name="obed_zs").update()
    Cena(typ="strava", display_name="Večeře VŠ", system_name="vecere_vs").update()
    Cena(typ="strava", display_name="Večeře ZŠ", system_name="vecere_zs").update()
    print("done")