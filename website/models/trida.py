from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Trida(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    short_name_cz = db.Column(db.String(300), nullable=False)
    full_name_cz = db.Column(db.String(1000))
    short_name_en = db.Column(db.String(300))
    full_name_en = db.Column(db.String(1000))
    capacity = db.Column(db.Integer, default=8)
    is_solo = db.Column(db.Boolean, default=True)
    is_free_as_secondary = db.Column(db.Boolean, default=False)
    age_group = db.Column(db.String(300), default="adult") #child, youth, adult
    
    tutor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tutor = db.relationship("User", back_populates="taught_classes", foreign_keys=[tutor_id])
    main_paticipants_priority_1 = db.relationship("User", back_populates="main_class_priority_1", foreign_keys="User.main_class_id_priority_1")
    main_paticipants_priority_2 = db.relationship("User", back_populates="main_class_priority_2", foreign_keys="User.main_class_id_priority_2")
    secondary_participants = db.relationship("User", back_populates="secondary_class", foreign_keys="User.secondary_class_id")

    def __repr__(self):
        return f"Třída | {self.short_name_cz}"

    def get_short_name_id_for_seznam(self):
        return {
            "id": self.id,
            "short_name": self.short_name_cz
        }
    
    def get_by_full_name(full_name: str) -> "Trida":
        #TODO tohle se mi nelibi, proc to tu je? je to z nacitani csvcek?
        return db.session.scalars(db.select(Trida).where(Trida.full_name_cz == full_name)).first()
    
    def info_pro_detail(self):
        #TODO tohle musi projit upravou prejmenovani atributu
        return {
            "short_name": self.short_name,
            "full_name": self.full_name,
            "hlavni_ucastnici_1": [{"name": u.get_full_name(), "link": "/organizator/ucastnik/" + str(u.id), "ucast": u.ucast} for u in sorted(self.hlavni_ucastnici_1, key=lambda u: u.prijmeni)],
            "hlavni_ucastnici_2": [{"name": u.get_full_name(), "link": "/organizator/ucastnik/" + str(u.id), "ucast": u.ucast} for u in sorted(self.hlavni_ucastnici_2, key=lambda u: u.prijmeni)],
            "vedlejsi_ucastnici_placeni": [{"name": u.get_full_name(), "link": "/organizator/ucastnik/" + str(u.id), "ucast": u.ucast} for u in sorted(self.vedlejsi_placena_ucastnici, key=lambda u: u.prijmeni)],
            "vedlejsi_ucastnici_zdarma": [{"name": u.get_full_name(), "link": "/organizator/ucastnik/" + str(u.id), "ucast": u.ucast} for u in sorted(self.vedlejsi_zdarma_ucastnici, key=lambda u: u.prijmeni)],
            "celkem": len(self.hlavni_ucastnici_1) + len(self.vedlejsi_placena_ucastnici) + len(self.vedlejsi_zdarma_ucastnici),
            "prvni_trida_count": len(self.hlavni_ucastnici_1),
            "druha_trida_count": len(self.hlavni_ucastnici_2),
            "vedlejsi_placena_count": len(self.vedlejsi_placena_ucastnici),
            "vedlejsi_zdarma_count": len(self.vedlejsi_zdarma_ucastnici)
        }
    
    def data_pro_upravu_ucastniku(self):
        return {
            "id": self.id,
            "full_name": self.full_name_cz,
        }
    
    def info_pro_upravu(self):
        return {
            "short_name_cz": self.short_name_cz,
            "full_name_cz": self.full_name_cz,
            "short_name_en": self.short_name_en,
            "full_name_en": self.full_name_en,
            "capacity": self.capacity,
            "age_group": self.age_group,
            "is_solo": "Ano" if self.is_solo else "Ne",
            "is_free_as_secondary": "Ano" if self.is_free_as_secondary else "Ne",
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
        