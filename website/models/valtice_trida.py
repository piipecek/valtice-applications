from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Valtice_trida(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String(300), nullable=False) # viz. vytvoreni_trid.py pro detail o tom, co v atributach cekat
    full_name = db.Column(db.String(1000), nullable=False, default="")
    je_zdarma_jako_vedlejsi = db.Column(db.Boolean, default=False)
    je_ansamblova = db.Column(db.Boolean, default=False)
    hlavni_ucastnici_1 = db.relationship('Valtice_ucastnik', backref='hlavni_trida_1', lazy=True, foreign_keys='Valtice_ucastnik.hlavni_trida_1_id')
    hlavni_ucastnici_2 = db.relationship('Valtice_ucastnik', backref='hlavni_trida_2', lazy=True, foreign_keys='Valtice_ucastnik.hlavni_trida_2_id')
    vedlejsi_placena_ucastnici = db.relationship('Valtice_ucastnik', backref='vedlejsi_trida_placena', lazy=True, foreign_keys='Valtice_ucastnik.vedlejsi_trida_placena_id')
    vedlejsi_zdarma_ucastnici = db.relationship('Valtice_ucastnik', backref='vedlejsi_trida_zdarma', lazy=True, foreign_keys='Valtice_ucastnik.vedlejsi_trida_zdarma_id')

    def get_short_name_id_for_seznam(self):
        return {
            "id": self.id,
            "short_name": self.short_name
        }
    
    def get_by_full_name(full_name: str) -> "Valtice_trida":
        return db.session.scalars(db.select(Valtice_trida).where(Valtice_trida.full_name == full_name)).first()
    
    def info_pro_detail(self):
        return {
            "short_name": self.short_name,
            "full_name": self.full_name,
            "hlavni_ucastnici_1": [{"name": u.get_full_name(), "link": "/valtice/ucastnik/" + str(u.id), "ucast": u.ucast} for u in sorted(self.hlavni_ucastnici_1, key=lambda u: u.prijmeni)],
            "hlavni_ucastnici_2": [{"name": u.get_full_name(), "link": "/valtice/ucastnik/" + str(u.id), "ucast": u.ucast} for u in sorted(self.hlavni_ucastnici_2, key=lambda u: u.prijmeni)],
            "vedlejsi_ucastnici_placeni": [{"name": u.get_full_name(), "link": "/valtice/ucastnik/" + str(u.id), "ucast": u.ucast} for u in sorted(self.vedlejsi_placena_ucastnici, key=lambda u: u.prijmeni)],
            "vedlejsi_ucastnici_zdarma": [{"name": u.get_full_name(), "link": "/valtice/ucastnik/" + str(u.id), "ucast": u.ucast} for u in sorted(self.vedlejsi_zdarma_ucastnici, key=lambda u: u.prijmeni)],
            "celkem": len(self.hlavni_ucastnici_1) + len(self.vedlejsi_placena_ucastnici) + len(self.vedlejsi_zdarma_ucastnici),
            "prvni_trida_count": len(self.hlavni_ucastnici_1),
            "druha_trida_count": len(self.hlavni_ucastnici_2),
            "vedlejsi_placena_count": len(self.vedlejsi_placena_ucastnici),
            "vedlejsi_zdarma_count": len(self.vedlejsi_zdarma_ucastnici)
        }
    
    def data_pro_upravu_ucastniku(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
        }
    
    def info_pro_upravu(self):
        if self.je_zdarma_jako_vedlejsi:
            typ = "zdarma"
        elif self.je_ansamblova:
            typ = "ansamblova"
        else:
            typ = "bezna"
        return {
            "short_name": self.short_name,
            "full_name": self.full_name,
            "typ": typ
        }
        
    def nacist_zmeny_z_requestu(self, request):
        self.short_name = request.form.get("short_name")
        self.full_name = request.form.get("full_name")
        if request.form.get("typ") == "bezna":
            self.je_zdarma_jako_vedlejsi = False
            self.je_ansamblova = False
        elif request.form.get("typ") == "ansamblova":
            self.je_zdarma_jako_vedlejsi = False
            self.je_ansamblova = True
        else:
            self.je_zdarma_jako_vedlejsi = True
            self.je_ansamblova = False
        self.update()
    
    def data_pro_seznamy(self):
        return {
            "id": self.id,
            "long_name": self.full_name
        }
        