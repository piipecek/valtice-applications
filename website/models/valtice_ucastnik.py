from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.helpers.pretty_date import pretty_datetime
from datetime import datetime
from flask_login import UserMixin
from website.models.valtice_trida import Valtice_trida
from website.models.cena import Cena

class Valtice_ucastnik(Common_methods_db_model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    cas = db.Column(db.DateTime, nullable=False)
    prijmeni = db.Column(db.String(100))
    jmeno = db.Column(db.String(100))
    vek = db.Column(db.String(50))
    email = db.Column(db.String(200))
    telefon = db.Column(db.String(100))
    finance_dne = db.Column(db.Date)
    finance_dar = db.Column(db.Float, default=0)
    finance_mena = db.Column(db.String(50), default="CZK")
    finance_kategorie = db.Column(db.String(100), default="dospely")
    finance_korekce_kurzovne = db.Column(db.Float, default=0)
    finance_korekce_kurzovne_duvod = db.Column(db.String(2000), default="")
    finance_korekce_strava = db.Column(db.Float, default=0)
    finance_korekce_strava_duvod = db.Column(db.String(2000), default="")
    finance_korekce_ubytko = db.Column(db.Float, default=0)
    finance_korekce_ubytko_duvod = db.Column(db.String(2000), default="")
    ssh_clen = db.Column(db.Boolean, default=False)
    ucast = db.Column(db.String(50), default="Aktivní")
    hlavni_trida_1_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    hlavni_trida_2_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    vedlejsi_trida_placena_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    vedlejsi_trida_zdarma_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    ubytovani = db.Column(db.String(1000), default="Nemá zájem")
    ubytovani_pocet = db.Column(db.Float, default=0)
    vzdelani = db.Column(db.String(2000)) 
    nastroj = db.Column(db.String(2000))
    repertoir = db.Column(db.String(2000))
    student_zus_valtice_mikulov = db.Column(db.Boolean)
    strava = db.Column(db.Boolean)
    strava_snidane_vinarska = db.Column(db.Integer, default=0)
    strava_snidane_zs = db.Column(db.Integer, default=0)
    strava_obed_vinarska_maso = db.Column(db.Integer, default=0)
    strava_obed_vinarska_vege = db.Column(db.Integer, default=0)
    strava_obed_zs_maso = db.Column(db.Integer, default=0)
    strava_obed_zs_vege = db.Column(db.Integer, default=0)
    strava_vecere_vinarska_maso = db.Column(db.Integer, default=0)
    strava_vecere_vinarska_vege = db.Column(db.Integer, default=0)
    strava_vecere_zs_maso = db.Column(db.Integer, default=0)
    strava_vecere_zs_vege = db.Column(db.Integer, default=0)
    uzivatelska_poznamka = db.Column(db.String(2000))
    admin_poznamka = db.Column(db.Text)
    cas_registrace = db.Column(db.DateTime)
    

    
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
            celkova_str = row[8]
            if "Kč" in celkova_str:
                mena = "CZK"
            elif "€" in celkova_str:
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
            
            # rok zaplaceni
            if row[7]:
                finance_dne = datetime.strptime(row[7], "%d.%m.")
                finance_dne = finance_dne.replace(year=2024)
            else:
                finance_dne = None
            
            # věková kategorie
            if row[45] in ["Student do 26 let", "Student up to 26"]:
                kategorie = "student"
            elif row[45] in ["Dítě do 15 let", "Children up to 15"]:
                kategorie = "dite"
            elif row[45] in ["Dospělý", "Other"]:
                kategorie = "dospely"
            else:
                print("Nepodařilo se určit věkovou kategorii ", row[45], row[2], row[3])
            
            
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
                    finance_dne=finance_dne, 
                    finance_dar=get_money_number(row[15]),
                    finance_mena=mena,
                    finance_kategorie=kategorie,
                    finance_korekce_kurzovne=get_money_number(row[16]) if row[16] else 0,
                    finance_korekce_kurzovne_duvod=row[17],
                    finance_korekce_strava=get_money_number(row[18]) if row[18] else 0,
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
                    admin_poznamka=row[43] + row[44],
                )
                novy_ucastnik.update()
                new += 1
                
                # kontrola kalkulace s csv
                kalkulace = novy_ucastnik.kalkulace()
                if kalkulace["celkem"] != get_money_number(row[8]):
                    print(f"Kalkulace účastníka {novy_ucastnik.jmeno} {novy_ucastnik.prijmeni} {pretty_datetime(novy_ucastnik.cas)} se neshoduje s csv: Očekávaná honota: {kalkulace['celkem']}, csv: {get_money_number(row[8])}, rozdíl = {kalkulace['celkem'] - get_money_number(row[8])}")
                
        return {"new": new, "skipped": skipped}
            
    def info_pro_seznam(self) -> dict:
        full_name = self.get_full_name()
        return {
            "id": self.id,
            "full_name": full_name if full_name else "-",
            "prijmeni": self.prijmeni if self.prijmeni else "-",
            "email": self.email if self.email else "-",
            "registrovan": "Registrován" if self.cas_registrace else "-",
            "hlavni_trida_1": Valtice_trida.get_by_id(self.hlavni_trida_1_id).short_name if self.hlavni_trida_1_id else "-",
            "hlavni_trida_1_id": self.hlavni_trida_1_id
        }
    
    def get_full_name(self) -> str:
        return f"{self.prijmeni} {self.jmeno}"
    
    def info_pro_detail(self):
        def pretty_penize(castka) -> str:
            if castka == 0:
                return "-"
            if castka == int(castka):
                castka = int(castka)
            else:
                castka = str(round(castka, 2)).replace(".", ",")
            if self.finance_mena == "CZK":
                return f"{castka} Kč"
            elif self.finance_mena == "EUR":
                return f"{castka} €"
         
        # display jidla
        list_pro_stravu_na_ocich = []
        snidane_list = []
        if self.strava_snidane_vinarska + self.strava_snidane_zs == 0:
            snidane = "-"
        if self.strava_snidane_zs != 0:
            snidane_list.append(f"ZŠ: {self.strava_snidane_zs}")
            list_pro_stravu_na_ocich.append(f"Snídaně ZŠ: {self.strava_snidane_zs}")
        if self.strava_snidane_vinarska != 0:
            snidane_list.append(f"VŠ: {self.strava_snidane_vinarska}")
            list_pro_stravu_na_ocich.append(f"Snídaně VŠ: {self.strava_snidane_vinarska}")
        if len(snidane_list) != 0:
            snidane = ", ".join(snidane_list)

        obed_list = []
        if self.strava_obed_vinarska_maso + self.strava_obed_vinarska_vege + self.strava_obed_zs_maso + self.strava_obed_zs_vege == 0:
            obed = "-"
        if self.strava_obed_zs_maso != 0:
            obed_list.append(f"ZŠ maso: {self.strava_obed_zs_maso}")
            list_pro_stravu_na_ocich.append(f"Oběd ZŠ maso: {self.strava_obed_zs_maso}")
        if self.strava_obed_zs_vege != 0:
            obed_list.append(f"ZŠ vege: {self.strava_obed_zs_vege}")
            list_pro_stravu_na_ocich.append(f"Oběd ZŠ vege: {self.strava_obed_zs_vege}")
        if self.strava_obed_vinarska_maso != 0:
            obed_list.append(f"VŠ maso: {self.strava_obed_vinarska_maso}")
            list_pro_stravu_na_ocich.append(f"Oběd VŠ maso: {self.strava_obed_vinarska_maso}")
        if self.strava_obed_vinarska_vege != 0:
            obed_list.append(f"VŠ vege: {self.strava_obed_vinarska_vege}")
            list_pro_stravu_na_ocich.append(f"Oběd VŠ vege: {self.strava_obed_vinarska_vege}")
        if len(obed_list) != 0:    
            obed = ", ".join(obed_list)
        
        vecere_list = []
        if self.strava_vecere_vinarska_maso + self.strava_vecere_vinarska_vege + self.strava_vecere_zs_maso + self.strava_vecere_zs_vege == 0:
            vecere = "-"
        if self.strava_vecere_zs_maso != 0:
            vecere_list.append(f"ZŠ maso: {self.strava_vecere_zs_maso}")
            list_pro_stravu_na_ocich.append(f"Večeře ZŠ maso: {self.strava_vecere_zs_maso}")
        if self.strava_vecere_zs_vege != 0:
            vecere_list.append(f"ZŠ vege: {self.strava_vecere_zs_vege}")
            list_pro_stravu_na_ocich.append(f"Večeře ZŠ vege: {self.strava_vecere_zs_vege}")
        if self.strava_vecere_vinarska_maso != 0:
            vecere_list.append(f"VŠ maso: {self.strava_vecere_vinarska_maso}")
            list_pro_stravu_na_ocich.append(f"Večeře VŠ maso: {self.strava_vecere_vinarska_maso}")
        if self.strava_vecere_vinarska_vege != 0:
            vecere_list.append(f"VŠ vege: {self.strava_vecere_vinarska_vege}")
            list_pro_stravu_na_ocich.append(f"Večeře VŠ vege: {self.strava_vecere_vinarska_vege}")
        if len(vecere_list) != 0:
            vecere = ", ".join(vecere_list)
            
        if len(list_pro_stravu_na_ocich) == 0:
            strava_na_ocich = "Nemá zájem"
        else:
            strava_na_ocich = ", ".join(list_pro_stravu_na_ocich)
            
        # ubytovani
        if self.ubytovani == "Nemá zájem":
            ubytovani = self.ubytovani
        else:
            if int(self.ubytovani_pocet) == self.ubytovani_pocet:
                pocet = int(self.ubytovani_pocet)
            else:
                pocet = self.ubytovani_pocet
            ubytovani = f"{self.ubytovani}: {pocet}"
            

                
        kalkulace = self.kalkulace()
        return {
            "cas": pretty_datetime(self.cas),
            "cas_registrace": pretty_datetime(self.cas_registrace) if self.cas_registrace else "Zatím neregistrován",
            "prijmeni": self.prijmeni,
            "jmeno": self.jmeno,
            "vek": self.vek if self.vek else "-",
            "email": self.email,
            "telefon": self.telefon if self.telefon else "-",
            "ssh_clen": "Ano" if self.ssh_clen else "Ne",
            "ucast": self.ucast,
            "ubytovani": ubytovani,
            "strava": "Má zájem, viz. níže" if self.strava else "Nemá zájem",
            "vzdelani": "-" if not self.vzdelani else self.vzdelani,
            "nastroj": "-" if not self.nastroj else self.nastroj,
            "repertoir": "-" if not self.repertoir else self.repertoir,
            "student_zus_valtice_mikulov": "Ano" if self.student_zus_valtice_mikulov else "Ne",
            "uzivatelska_poznamka": self.uzivatelska_poznamka if self.uzivatelska_poznamka else "-",
            "admin_poznamka": self.admin_poznamka if self.admin_poznamka else "-",
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
            },
            "finance_dne": pretty_datetime(self.finance_dne) if self.finance_dne else "Zatím neplaceno",
            "finance_celkem": pretty_penize(kalkulace["celkem"]),
            "finance_trida_1": pretty_penize(kalkulace["prvni_trida"]),
            "finance_trida_2": pretty_penize(kalkulace["vedlejsi_trida"]),
            "finance_ubytovani": pretty_penize(kalkulace["ubytovani"]),
            "finance_snidane": pretty_penize(kalkulace["snidane"]),
            "finance_obedy": pretty_penize(kalkulace["obedy"]),
            "finance_vecere": pretty_penize(kalkulace["vecere"]),
            "finance_dar": pretty_penize(kalkulace["dar"]),
            "finance_korekce_kurzovne": pretty_penize(self.finance_korekce_kurzovne),
            "finance_korekce_strava": pretty_penize(self.finance_korekce_strava),
            "finance_korekce_ubytko": pretty_penize(self.finance_korekce_ubytko),
            "finance_korekce_kurzovne_duvod": self.finance_korekce_kurzovne_duvod if self.finance_korekce_kurzovne_duvod else "-",
            "finance_korekce_strava_duvod": self.finance_korekce_strava_duvod if self.finance_korekce_strava_duvod else "-",
            "finance_korekce_ubytko_duvod": self.finance_korekce_ubytko_duvod if self.finance_korekce_ubytko_duvod else "-",
            "strava_snidane": snidane,
            "strava_obedy": obed,
            "strava_vecere": vecere,
            "strava_na_ocich": strava_na_ocich,
        }
    
    @staticmethod
    def novy_ucastnik_from_admin(jmeno, prijmeni) -> int:
        v = Valtice_ucastnik()
        v.jmeno = jmeno
        v.prijmeni = prijmeni
        v.cas = datetime.now()
        v.update()
        return v.id
    
    def kalkulace(self) -> dict:
        # ubytovani
        if self.ubytovani in ["Tělocvična", "Tělocvična (náhradník)"]:
            if self.finance_mena == "CZK":        
                ubytko = self.ubytovani_pocet * Cena.get_by_system_name("telocvicna").czk
            elif self.finance_mena == "EUR":
                ubytko = self.ubytovani_pocet * Cena.get_by_system_name("telocvicna").eur
        elif self.ubytovani == "Internát vinařské školy":
            if self.finance_mena == "CZK":
                ubytko = self.ubytovani_pocet * Cena.get_by_system_name("internat").czk
            elif self.finance_mena == "EUR":
                ubytko = self.ubytovani_pocet * Cena.get_by_system_name("internat").eur
        else:
            ubytko = 0
        
        # kurzovne
        def vycislit(ucast: str, mena: str, kategorie: str, clen_ssh: bool, cislo_tridy: int, trida: Valtice_trida) -> int:
            if trida is None:
                return 0
            if cislo_tridy == 1:
                if ucast == "Pasivní":
                    if mena == "CZK":
                        return Cena.get_by_system_name("kurzovne_pasivni").czk
                    elif mena == "EUR":
                        return Cena.get_by_system_name("kurzovne_pasivni").eur
                if kategorie == "dite":
                    if mena == "CZK":
                        return Cena.get_by_system_name("kurzovne_deti").czk
                    elif mena == "EUR":
                        return Cena.get_by_system_name("kurzovne_deti").eur
                elif kategorie == "student":
                    if mena == "CZK":
                        return Cena.get_by_system_name("kurzovne_student").czk
                    elif mena == "EUR":
                        return Cena.get_by_system_name("kurzovne_student").eur
                elif clen_ssh:
                    if mena == "CZK":
                        return Cena.get_by_system_name("kurzovne_ssh").czk
                    elif mena == "EUR":
                        return Cena.get_by_system_name("kurzovne_ssh").eur
                elif kategorie == "dospely":
                    if mena == "CZK":
                        return Cena.get_by_system_name("kurzovne").czk
                    elif mena == "EUR":
                        return Cena.get_by_system_name("kurzovne").eur
            elif cislo_tridy == 2:
                if trida.je_zdarma_jako_vedlejsi:
                    return 0
                elif trida.je_ansamblova:
                    if mena == "CZK":
                        return Cena.get_by_system_name("ansambly").czk
                    elif mena == "EUR":
                        return Cena.get_by_system_name("ansambly").eur
                else:
                    return vycislit(ucast, mena, kategorie, clen_ssh, 1, trida)
        
        prvni_trida = vycislit(self.ucast, self.finance_mena, self.finance_kategorie, self.ssh_clen, 1, self.hlavni_trida_1)
        vedlejsi_trida_placena = vycislit(self.ucast, self.finance_mena, self.finance_kategorie, self.ssh_clen, 2, self.vedlejsi_trida_placena)
        
        
        # strava
        if self.finance_mena == "CZK":
            snidane = self.strava_snidane_zs * Cena.get_by_system_name("snidane_zs").czk + self.strava_snidane_vinarska * Cena.get_by_system_name("snidane_ss").czk
            obedy = self.strava_obed_zs_maso * Cena.get_by_system_name("obed_zs").czk + self.strava_obed_zs_vege * Cena.get_by_system_name("obed_zs").czk + self.strava_obed_vinarska_maso * Cena.get_by_system_name("obed_ss").czk + self.strava_obed_vinarska_vege * Cena.get_by_system_name("obed_ss").czk
            vecere = self.strava_vecere_zs_maso * Cena.get_by_system_name("vecere_zs").czk + self.strava_vecere_zs_vege * Cena.get_by_system_name("vecere_zs").czk + self.strava_vecere_vinarska_maso * Cena.get_by_system_name("vecere_ss").czk + self.strava_vecere_vinarska_vege * Cena.get_by_system_name("vecere_ss").czk
        elif self.finance_mena == "EUR":
            snidane = self.strava_snidane_zs * Cena.get_by_system_name("snidane_zs").eur + self.strava_snidane_vinarska * Cena.get_by_system_name("snidane_ss").eur
            obedy = self.strava_obed_zs_maso * Cena.get_by_system_name("obed_zs").eur + self.strava_obed_zs_vege * Cena.get_by_system_name("obed_zs").eur + self.strava_obed_vinarska_maso * Cena.get_by_system_name("obed_ss").eur + self.strava_obed_vinarska_vege * Cena.get_by_system_name("obed_ss").eur
            vecere = self.strava_vecere_zs_maso * Cena.get_by_system_name("vecere_zs").eur + self.strava_vecere_zs_vege * Cena.get_by_system_name("vecere_zs").eur + self.strava_vecere_vinarska_maso * Cena.get_by_system_name("vecere_ss").eur + self.strava_vecere_vinarska_vege * Cena.get_by_system_name("vecere_ss").eur
        
        result = {
            "ubytovani": ubytko,
            "prvni_trida": prvni_trida,
            "vedlejsi_trida": vedlejsi_trida_placena,
            "snidane": snidane,
            "obedy": obedy,
            "vecere": vecere,
            "dar": self.finance_dar,
            "celkem": ubytko + snidane + obedy + vecere + self.finance_dar + prvni_trida + vedlejsi_trida_placena + self.finance_korekce_kurzovne + self.finance_korekce_strava + self.finance_korekce_ubytko
        }
        return result

    def info_pro_upravu(self):
        return {
            "prijmeni": self.prijmeni,
            "jmeno": self.jmeno,
            "vek": self.vek,
            "email": self.email,
            "telefon": self.telefon,
            "finance_dne": self.finance_dne.isoformat() if self.finance_dne else None,
            "finance_dar": self.finance_dar,
            "finance_mena": self.finance_mena,
            "finance_kategorie": self.finance_kategorie,
            "finance_korekce_kurzovne": self.finance_korekce_kurzovne,
            "finance_korekce_kurzovne_duvod": self.finance_korekce_kurzovne_duvod,
            "finance_korekce_strava": self.finance_korekce_strava,
            "finance_korekce_strava_duvod": self.finance_korekce_strava_duvod,
            "finance_korekce_ubytko": self.finance_korekce_ubytko,
            "finance_korekce_ubytko_duvod": self.finance_korekce_ubytko_duvod,
            "ssh_clen": "Ano" if self.ssh_clen else "Ne", # takhle se to rovnou priradi ke spravnymu option v select 
            "ucast": self.ucast,
            "hlavni_trida_1": self.hlavni_trida_1_id,
            "hlavni_trida_2": self.hlavni_trida_2_id,
            "vedlejsi_trida_placena": self.vedlejsi_trida_placena_id,
            "vedlejsi_trida_zdarma": self.vedlejsi_trida_zdarma_id,
            "ubytovani": self.ubytovani,
            "ubytovani_pocet": self.ubytovani_pocet,
            "vzdelani": self.vzdelani,
            "nastroj": self.nastroj,
            "repertoir": self.repertoir,
            "student_zus_valtice_mikulov": "Ano" if self.student_zus_valtice_mikulov else "Ne",
            "strava": "Ano" if self.strava else "Ne",
            "strava_snidane_vinarska": self.strava_snidane_vinarska,
            "strava_snidane_zs": self.strava_snidane_zs,
            "strava_obed_vinarska_maso": self.strava_obed_vinarska_maso,
            "strava_obed_vinarska_vege": self.strava_obed_vinarska_vege,
            "strava_obed_zs_maso": self.strava_obed_zs_maso,
            "strava_obed_zs_vege": self.strava_obed_zs_vege,
            "strava_vecere_vinarska_maso": self.strava_vecere_vinarska_maso,
            "strava_vecere_vinarska_vege": self.strava_vecere_vinarska_vege,
            "strava_vecere_zs_maso": self.strava_vecere_zs_maso,
            "strava_vecere_zs_vege": self.strava_vecere_zs_vege,
            "uzivatelska_poznamka": self.uzivatelska_poznamka,
            "admin_poznamka": self.admin_poznamka,
            "cas_registrace": pretty_datetime(self.cas_registrace) if self.cas_registrace else None,
        }
    
    def nacist_zmeny_z_requestu(self, request):
        self.jmeno = request.form.get("jmeno")
        self.prijmeni = request.form.get("prijmeni")
        self.vek = request.form.get("vek")
        self.email = request.form.get("email")
        self.telefon = request.form.get("telefon")
        self.finance_dne = datetime.strptime(request.form.get("finance_dne"), "%Y-%m-%d") if request.form.get("finance_dne") else None
        self.finance_dar = float(request.form.get("finance_dar"))
        self.finance_mena = request.form.get("finance_mena")
        self.finance_kategorie = request.form.get("finance_kategorie")
        self.finance_korekce_kurzovne = float(request.form.get("finance_korekce_kurzovne"))
        self.finance_korekce_kurzovne_duvod = request.form.get("finance_korekce_kurzovne_duvod")
        self.finance_korekce_strava = float(request.form.get("finance_korekce_strava"))
        self.finance_korekce_strava_duvod = request.form.get("finance_korekce_strava_duvod")
        self.finance_korekce_ubytko = float(request.form.get("finance_korekce_ubytko"))
        self.finance_korekce_ubytko_duvod = request.form.get("finance_korekce_ubytko_duvod")
        self.ssh_clen = True if request.form.get("ssh_clen") == "Ano" else False
        self.ucast = request.form.get("ucast")
        self.hlavni_trida_1_id = int(request.form.get("hlavni_trida_1")) if request.form.get("hlavni_trida_1") != "-" else None
        self.hlavni_trida_2_id = int(request.form.get("hlavni_trida_2")) if request.form.get("hlavni_trida_2") != "-" else None
        self.vedlejsi_trida_placena_id = int(request.form.get("vedlejsi_trida_placena")) if request.form.get("vedlejsi_trida_placena") != "-" else None
        self.vedlejsi_trida_zdarma_id = int(request.form.get("vedlejsi_trida_zdarma")) if request.form.get("vedlejsi_trida_zdarma") != "-" else None
        self.ubytovani = request.form.get("ubytovani")
        self.ubytovani_pocet = float(request.form.get("ubytovani_pocet"))
        self.vzdelani = request.form.get("vzdelani")
        self.nastroj = request.form.get("nastroj")
        self.repertoir = request.form.get("repertoir")
        self.student_zus_valtice_mikulov = True if request.form.get("student_zus_valtice_mikulov") == "Ano" else False
        self.strava = True if request.form.get("strava") == "Ano" else False
        self.strava_snidane_vinarska = int(request.form.get("strava_snidane_vinarska")) if request.form.get("strava_snidane_vinarska") else 0
        self.strava_snidane_zs = int(request.form.get("strava_snidane_zs")) if request.form.get("strava_snidane_zs") else 0
        self.strava_obed_vinarska_maso = int(request.form.get("strava_obed_vinarska_maso")) if request.form.get("strava_obed_vinarska_maso") else 0
        self.strava_obed_vinarska_vege = int(request.form.get("strava_obed_vinarska_vege")) if request.form.get("strava_obed_vinarska_vege") else 0
        self.strava_obed_zs_maso = int(request.form.get("strava_obed_zs_maso")) if request.form.get("strava_obed_zs_maso") else 0
        self.strava_obed_zs_vege = int(request.form.get("strava_obed_zs_vege")) if request.form.get("strava_obed_zs_vege") else 0
        self.strava_vecere_vinarska_maso = int(request.form.get("strava_vecere_vinarska_maso")) if request.form.get("strava_vecere_vinarska_maso") else 0
        self.strava_vecere_vinarska_vege = int(request.form.get("strava_vecere_vinarska_vege")) if request.form.get("strava_vecere_vinarska_vege") else 0
        self.strava_vecere_zs_maso = int(request.form.get("strava_vecere_zs_maso")) if request.form.get("strava_vecere_zs_maso") else 0
        self.strava_vecere_zs_vege = int(request.form.get("strava_vecere_zs_vege")) if request.form.get("strava_vecere_zs_vege") else 0
        self.uzivatelska_poznamka = request.form.get("uzivatelska_poznamka")
        self.admin_poznamka = request.form.get("admin_poznamka")
        self.update()