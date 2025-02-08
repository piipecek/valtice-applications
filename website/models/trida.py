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

    def info_pro_seznam_trid(self):
        return {
            "id": self.id,
            "short_name": self.short_name_cz,
            "tutor_full_name": self.tutor.get_full_name() if self.tutor else "Zatím bez lektora",
            "tutor_id": self.tutor_id,
        }
    
    def get_by_full_name(full_name: str) -> "Trida":
        #TODO tohle se mi nelibi, proc to tu je? je to z nacitani csvcek?
        return db.session.scalars(db.select(Trida).where(Trida.full_name_cz == full_name)).first()
    
    def info_pro_detail(self):
        if self.age_group == "child":
            age_group = "dětská"
        elif self.age_group == "youth":
            age_group = "mládež do 15 let"
        else:
            age_group = "dospělá"
        
        tutor = "Zatím bez lektora"
        if self.tutor:
            tutor = self.tutor.get_full_name()
            
        return {
            "tutor": {
                "name": tutor,
                "id": self.tutor_id,
            },
            "short_name_cz": self.short_name_cz,
            "full_name_cz": self.full_name_cz if self.full_name_cz else "-",
            "short_name_en": self.short_name_en if self.short_name_en else "-",
            "full_name_en": self.full_name_en if self.full_name_en else "-",
            "capacity": self.capacity if self.capacity else "-",
            "is_solo": "sólová" if self.is_solo else "hromadná",
            "is_free_as_secondary": "Ano" if self.is_free_as_secondary else "Ne",
            "age_group": age_group,
            "main_participants_priority_1": [{"name": u.get_full_name(), "link": "/organizator/detail_ucastnika/" + str(u.id), "ucast": "aktivní" if u.is_active_participant else "pasivní"} for u in sorted(self.main_paticipants_priority_1, key=lambda u: u.surname)],
            "main_participants_priority_2": [{"name": u.get_full_name(), "link": "/organizator/detail_ucastnika/" + str(u.id), "ucast": "aktivní" if u.is_active_participant else "pasivní"} for u in sorted(self.main_paticipants_priority_2, key=lambda u: u.surname)],
            "secondary_participants": [{"name": u.get_full_name(), "link": "/organizator/detail_ucastnika/" + str(u.id), "ucast": "aktivní" if u.is_active_participant else "pasivní"} for u in sorted(self.secondary_participants, key=lambda u: u.surname)],
            "main_participants_priority_1_count": len(self.main_paticipants_priority_1),
            "main_participants_priority_2_count": len(self.main_paticipants_priority_2),
            "secondary_participants_count": len(self.secondary_participants),
        }
    
    def data_pro_upravu_ucastniku(self):
        return {
            "id": self.id,
            "full_name_cz": self.full_name_cz,
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
            "tutor_id": self.tutor_id if self.tutor_id else "-",
        }
        
    def nacist_zmeny_z_requestu(self, request):
        self.short_name_cz = request.form.get("short_name_cz")
        self.full_name_cz = request.form.get("full_name_cz")
        self.short_name_en = request.form.get("short_name_en")
        self.full_name_en = request.form.get("full_name_en")
        self.capacity = int(request.form.get("capacity"))
        self.age_group = request.form.get("age_group")
        self.is_solo = request.form.get("is_solo") == "Ano"
        self.is_free_as_secondary = request.form.get("is_free_as_secondary") == "Ano"
        self.tutor_id = int(request.form.get("tutor_id")) if request.form.get("tutor_id") != "-" else None
        self.update()
        
    
    def data_pro_seznamy(self):
        return {
            "id": self.id,
            "long_name": self.full_name
        }
        