# v jednu chvili bylo potreba prehodit znaminka korekci tak, aby kladna korekce skutence pricitala a zaporna odecitala

from website import create_app
from website.models.valtice_ucastnik import Valtice_ucastnik

app = create_app()
with app.app_context():
    for u in Valtice_ucastnik.get_all():
        u: Valtice_ucastnik
        if u.finance_korekce_kurzovne:
            u.finance_korekce_kurzovne = -u.finance_korekce_kurzovne
            print(f"Změněna korekce kurzovného u {u.prijmeni} {u.jmeno} na {u.finance_korekce_kurzovne}")
        if u.finance_korekce_ubytko:
            u.finance_korekce_ubytko = -u.finance_korekce_ubytko
            print(f"Změněna korekce ubytování u {u.prijmeni} {u.jmeno} na {u.finance_korekce_ubytko}")
        if u.finance_korekce_strava:
            u.finance_korekce_strava = -u.finance_korekce_strava
            print(f"Změněna korekce stravy u {u.prijmeni} {u.jmeno} na {u.finance_korekce_strava}")
        u.update()
    print("done")