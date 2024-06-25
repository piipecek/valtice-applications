from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from website.helpers.pretty_date import pretty_datetime
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_login import UserMixin, current_user, login_user
from typing import List
import jwt
from website.models.valtice_trida import Valtice_trida
import unicodedata

class Valtice_ucastnik(Common_methods_db_model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    cas = db.Column(db.DateTime, nullable=False)
    prijmeni = db.Column(db.String(100))
    jmeno = db.Column(db.String(100))
    vek = db.Column(db.String(50))
    email = db.Column(db.String(200))
    telefon = db.Column(db.String(100))
    finance_dne = db.Column(db.DateTime)
    finance_dar = db.Column(db.Float)
    finance_mena = db.Column(db.String(50))
    finance_korekce_kurzovne = db.Column(db.Float)
    finance_korekce_kurzovne_duvod = db.Column(db.String(2000))
    finance_korekce_strava = db.Column(db.Float)
    finance_korekce_strava_duvod = db.Column(db.String(2000))
    ssh_clen = db.Column(db.Boolean)
    ucast = db.Column(db.String(50))
    hlavni_trida_1_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    hlavni_trida_2_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    vedlejsi_trida_placena_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    vedlejsi_trida_zdarma_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    ubytovani = db.Column(db.String(1000))
    ubytovani_pocet = db.Column(db.Integer)
    vzdelani = db.Column(db.String(2000)) 
    nastroj = db.Column(db.String(2000))
    repertoir = db.Column(db.String(2000))
    student_zus_valtice_mikulov = db.Column(db.Boolean)
    strava = db.Column(db.Boolean)
    strava_snidane_vinarska = db.Column(db.Integer)
    strava_snidane_zs = db.Column(db.Integer)
    strava_obed_vinarska_maso = db.Column(db.Integer)
    strava_obed_vinarska_vege = db.Column(db.Integer)
    strava_obed_zs_maso = db.Column(db.Integer)
    strava_obed_zs_vege = db.Column(db.Integer)
    strava_vecere_vinarska_maso = db.Column(db.Integer)
    strava_vecere_vinarska_vege = db.Column(db.Integer)
    strava_vecere_zs_maso = db.Column(db.Integer)
    strava_vecere_zs_vege = db.Column(db.Integer)
    uzivatelska_poznamka = db.Column(db.String(2000))
    admin_poznamka = db.Column(db.Text)
    registrovan_dne = db.Column(db.DateTime)
    
    
    
    
    def __repr__(self) -> str:
        return f"Uživatel | {self.email}"


    @staticmethod
    def is_duplicate_ucastnik(time, prijmeni, jmeno, email) -> bool:
        return db.session.scalars(db.select(Valtice_ucastnik).where(Valtice_ucastnik.cas == time, Valtice_ucastnik.jmeno == jmeno, Valtice_ucastnik.prijmeni == prijmeni, Valtice_ucastnik.email == email)).first()
    
    
    @staticmethod    
    def vytvorit_nove_ucastniky_z_csv(csv_file: list[list[str]]) -> None:
        new = 0
        skipped = 0
        for row in csv_file[1:]:# skip first row
            
            cas = datetime.strptime(row[1], "%d.%m.%Y %H:%M:%S")
            
            # měna
            dar_str = row[15]
            if "Kč" in dar_str:
                mena = "CZK"
            elif "€" in dar_str:
                mena = "EUR"
            
            # převod na čísla
            def get_money_number(money_str: str) -> float:
                if money_str == "":
                    return 0
                money_str = money_str.replace(u"\xa0", u"").replace("Kč", "").replace("€", "").replace(",", ".").replace(" ", "").strip()
                return float(money_str)
            
            # ubytování
            if row[25] == "Tělocvična":
                ubytovani = "Tělocvična"
            elif row[25] == "Internát vinařské školy":
                ubytovani = "Internát vinařské školy"
            elif row[25] in ["Nemám zájem", "I'm not interested"]:
                ubytovani = "Nemá zájem"
            elif row[25] == "Tělocvična (náhradník)":
                ubytovani = "Tělocvična (náhradník)"
            else:
                print("Nepodařilo se určit ubytování ", row[25])
            
            if get_money_number(row[11]) in [1280, 3600, 145, 55]:
                pocet = 1
            elif get_money_number(row[11]) == 0:
                pocet = 0
            else:
                print("Je potřeba korekce ceny ubytka pro účastníka ", row[2], row[3])
            
            
            
            # sjednocení poznámek
            pozn1 = row[41]
            pozn2 = row[42]
            if all([pozn1, pozn2]):
                poznamka = f"1. dotazník: {pozn1}, 2. dotazník: {pozn2}"
            else:
                poznamka = pozn1 if pozn1 else pozn2
                
            # tridy
            for trida in [row[22], row[23], row[24]]:
                if trida:
                    if trida == "Nemám zájem" or trida == "I'm not interested":
                        continue
                    elif not Valtice_trida.get_by_full_name(trida):
                        print("Nepodařilo se najít třídu ", trida)
            
            if Valtice_ucastnik.is_duplicate_ucastnik(cas, row[2], row[3], row[5]):
                skipped += 1 
                continue
            else:
                novy_ucastnik = Valtice_ucastnik(
                    cas=cas,
                    prijmeni=row[2], 
                    jmeno=row[3],
                    vek=row[4],
                    email=row[5],
                    telefon=row[6],
                    finance_dne=datetime.strptime(row[7], "%d.%m.") if row[7] else None, 
                    finance_dar=get_money_number(row[15]),
                    finance_mena=mena,
                    finance_korekce_kurzovne=get_money_number(row[16]) if row[16] else None,
                    finance_korekce_kurzovne_duvod=row[17],
                    finance_korekce_strava=get_money_number(row[18]) if row[18] else None,
                    finance_korekce_strava_duvod=row[19],
                    ssh_clen=True if row[20] in ["Ano", "Yes"] else False,
                    ucast="Aktivní" if row[21] in ["Active", "Aktivní"] else "Pasivní",
                    hlavni_trida_1_id = Valtice_trida.get_by_full_name(row[22]).id if Valtice_trida.get_by_full_name(row[22]) else None,
                    #hlavni_trida_2_id = Valtice_trida.get_by_full_name(row[10]).id if Valtice_trida.get_by_full_name(row[10]) else None,
                    vedlejsi_trida_placena_id = Valtice_trida.get_by_full_name(row[23]).id if Valtice_trida.get_by_full_name(row[23]) else None,
                    vedlejsi_trida_zdarma_id = Valtice_trida.get_by_full_name(row[24]).id if Valtice_trida.get_by_full_name(row[24]) else None,
                    ubytovani=ubytovani,
                    ubytovani_pocet=pocet,
                    vzdelani=row[26],
                    nastroj=row[27],
                    repertoir=row[28],
                    student_zus_valtice_mikulov=True if row[29] in ["Ano", "Yes"] else False,
                    strava=True if row[30] in ["Ano", "Yes"] else False,
                    strava_snidane_vinarska=int(row[31]) if row[31] else 0,
                    strava_snidane_zs=int(row[32]) if row[32] else 0,
                    strava_obed_vinarska_maso=int(row[33]) if row[33] else 0,
                    strava_obed_vinarska_vege=int(row[34]) if row[34] else 0,
                    strava_obed_zs_maso=int(row[35]) if row[35] else 0,
                    strava_obed_zs_vege=int(row[36]) if row[36] else 0,
                    strava_vecere_vinarska_maso=int(row[37]) if row[37] else 0,
                    strava_vecere_vinarska_vege=int(row[38]) if row[38] else 0,
                    strava_vecere_zs_maso=int(row[39]) if row[39] else 0,
                    strava_vecere_zs_vege=int(row[40]) if row[40] else 0,
                    uzivatelska_poznamka=poznamka,
                    admin_poznamka=row[42],
                )
                novy_ucastnik.update()
                new += 1
        return {"new": new, "skipped": skipped}
            
    def info_pro_seznam(self) -> dict:
        full_name = self.get_full_name()
        return {
            "id": self.id,
            "full_name": full_name,
            "prijmeni": self.prijmeni,
            "email": self.email,
            "telefon": self.telefon,
            "hlavni_trida_1": Valtice_trida.get_by_id(self.hlavni_trida_1_id).short_name if self.hlavni_trida_1_id else "-",
        }
    
    def get_full_name(self) -> str:
        return f"{self.prijmeni} {self.jmeno}"
    
    def info_pro_detail(self):
        return {
            "id": self.id,
            "cas": pretty_datetime(self.cas),
            "osloveni": self.osloveni,
            "prijmeni": self.prijmeni,
            "jmeno": self.jmeno,
            "vek": self.vek,
            "email": self.email,
            "telefon": self.telefon,
            "ssh_clen": "Ano" if self.ssh_clen else "Ne",
            "ucast": self.ucast,
            "ubytovani": self.ubytovani,
            "strava": self.strava,
            "prispevek": self.prispevek,
            "poznamka": self.poznamka,
            "vzdelani": self.vzdelani,
            "hlavni_trida_1": {
                "name": Valtice_trida.get_by_id(self.hlavni_trida_1_id).full_name if self.hlavni_trida_1_id else "-",
                "link": "/valtice/trida/" + str(self.hlavni_trida_1_id) if self.hlavni_trida_1_id else None
            },
            "hlavni_trida_2": {
                "name": Valtice_trida.get_by_id(self.hlavni_trida_2_id).full_name if self.hlavni_trida_2_id else "-",
                "link": "/valtice/trida/" + str(self.hlavni_trida_2_id) if self.hlavni_trida_2_id else None
            },
            "vedlejsi_trida_placena": {
                "name": Valtice_trida.get_by_id(self.vedlejsi_trida_placena_id).full_name if self.vedlejsi_trida_placena_id else "-",
                "link": "/valtice/trida/" + str(self.vedlejsi_trida_placena_id) if self.vedlejsi_trida_placena_id else None
            },
            "vedlejsi_trida_zdarma": {
                "name": Valtice_trida.get_by_id(self.vedlejsi_trida_zdarma_id).full_name if self.vedlejsi_trida_zdarma_id else "-",
                "link": "/valtice/trida/" + str(self.vedlejsi_trida_zdarma_id) if self.vedlejsi_trida_zdarma_id else None
            }
        }
    
    @staticmethod
    def novy_ucastnik_from_admin(jmeno, prijmeni):
        v = Valtice_ucastnik()
        v.jmeno = jmeno
        v.prijmeni = prijmeni
        v.cas = datetime.now()
        v.update()