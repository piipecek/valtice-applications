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

class Valtice_ucastnik(Common_methods_db_model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    cas = db.Column(db.DateTime, nullable=False)
    osloveni = db.Column(db.String(50))
    prijmeni = db.Column(db.String(100))
    jmeno = db.Column(db.String(100))
    vek = db.Column(db.String(50))
    email = db.Column(db.String(100))
    telefon = db.Column(db.String(100))
    ssh_clen = db.Column(db.Boolean)
    ucast = db.Column(db.String(50))
    ubytovani = db.Column(db.String(1000))
    strava = db.Column(db.String(100))
    prispevek = db.Column(db.String(2000))
    poznamka = db.Column(db.String(2000))
    vzdelani = db.Column(db.String(2000))
    hlavni_trida_1_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    hlavni_trida_2_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    vedlejsi_trida_placena_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    vedlejsi_trida_zdarma_id = db.Column(db.Integer, db.ForeignKey('valtice_trida.id'))
    
    def __repr__(self) -> str:
        return f"Uživatel | {self.email}"


    @staticmethod
    def is_duplicate_ucastnik(time, prijmeni, jmeno) -> bool:
        return db.session.scalars(db.select(Valtice_ucastnik).where(Valtice_ucastnik.cas == time, Valtice_ucastnik.jmeno == jmeno, Valtice_ucastnik.prijmeni == prijmeni)).first()
    
    
    @staticmethod
    def vytvorit_nove_ucastniky_z_csv(csv_file: list[list[str]]) -> None:
        new = 0
        skipped = 0
        for row in csv_file[1:]:# skip first row
            cas = datetime.strptime(row[0], "%d.%m.%Y %H:%M:%S")
            if Valtice_ucastnik.is_duplicate_ucastnik(cas, row[2], row[3]):
                skipped += 1
                continue
            else:
                novy_ucastnik = Valtice_ucastnik(
                    cas=cas,
                    osloveni=row[1],
                    prijmeni=row[2],
                    jmeno=row[3],
                    vek=row[4],
                    email=row[5],
                    telefon=row[6],
                    ssh_clen=True if row[7] in ["Ano", "Yes"] else False,
                    ucast="Aktivní" if row[8] in ["Active", "Aktivní"] else "Pasivní",
                    ubytovani=row[13],
                    strava=row[14],
                    prispevek=row[15],
                    poznamka=row[16],
                    vzdelani=row[17],
                    hlavni_trida_1_id = Valtice_trida.get_by_full_name(row[9]).id if Valtice_trida.get_by_full_name(row[9]) else None,
                    hlavni_trida_2_id = Valtice_trida.get_by_full_name(row[10]).id if Valtice_trida.get_by_full_name(row[10]) else None,
                    vedlejsi_trida_placena_id = Valtice_trida.get_by_full_name(row[11]).id if Valtice_trida.get_by_full_name(row[11]) else None,
                    vedlejsi_trida_zdarma_id = Valtice_trida.get_by_full_name(row[12]).id if Valtice_trida.get_by_full_name(row[12]) else None
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
            "hlavni_trida_1": Valtice_trida.get_by_id(self.hlavni_trida_1_id).short_name,
        }
    
    def get_full_name(self) -> str:
        return f"{self.prijmeni} {self.jmeno}"
    
    def info_pro_detail(self):
        print(self.cas, type(self.cas))
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