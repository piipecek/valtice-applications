from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from flask_login import current_user
import czech_sort
from website.helpers.pretty_date import pretty_datetime


user_secondary_class_jointable = db.Table(
    "user_secondary_class_jointable",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("class_id", db.Integer, db.ForeignKey("trida.id"), primary_key=True)
)


class Trida(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    discipline_cz = db.Column(db.String(1000))
    discipline_en = db.Column(db.String(1000))
    capacity = db.Column(db.Integer, default=8)
    has_capacity = db.Column(db.Boolean, default=True)
    secondary_billing_behavior = db.Column(db.String(300), default="full") # full, free, ensemble
    is_time_exclusive = db.Column(db.Boolean, default=False)
    age_group = db.Column(db.String(300), default="adult") # child, adult, both
    
    tutor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tutor = db.relationship("User", back_populates="taught_classes", foreign_keys=[tutor_id])
    primary_participants = db.relationship("User", back_populates="primary_class", foreign_keys="User.primary_class_id")
    secondary_participants = db.relationship("User",secondary=user_secondary_class_jointable, back_populates="secondary_classes")


    def __repr__(self):
        return f"Třída | {self.discipline_cz}"
    
    
    def get_name_cz(self) -> str:
        if self.discipline_cz and self.tutor:
            return f"{self.tutor.get_full_name('cz')} - {self.discipline_cz}"
        elif self.tutor:
            return self.tutor.get_full_name('cz')
        elif self.discipline_cz:
            return self.discipline_cz
        else:
            return "Chybí název třídy"
    
    
    def get_name_en(self) -> str:
        if self.discipline_en and self.tutor:
            return f"{self.tutor.get_full_name('en')} - {self.discipline_en}"
        elif self.tutor:
            return self.tutor.get_full_name('en')
        elif self.discipline_en:
            return self.discipline_en
        else:
            return "The name of the class is missing"
    

    def info_for_admin_class_list(self):
        pocet_ucastniku = str(len(self.primary_participants) + len(self.secondary_participants)) + "/" + str(self.capacity)
        if not self.has_capacity:
            pocet_ucastniku = str(len(self.primary_participants) + len(self.secondary_participants))
        return {
            "id": self.id,
            "discipline": self.discipline_cz,
            "tutor_full_name": self.tutor.get_full_name("cz") if self.tutor else "Zatím bez lektora",
            "tutor_id": self.tutor_id,
            "pocet_ucastniku": pocet_ucastniku
        }
        
    
    def info_for_admin_detail(self):
        if self.age_group == "child":
            age_group = "Do 15 let včetně"
        elif self.age_group == "adult":
            age_group = "Od 16 let"
        elif self.age_group == "both":
            age_group = "Smíšená - pro děti i dospělé"
            
        secondary_billing_behavior = "Zdarma"
        if self.secondary_billing_behavior == "full":
            secondary_billing_behavior = "Plně placená"
        elif self.secondary_billing_behavior == "ensemble":
            secondary_billing_behavior = "Placená jako komorní a ansámblová"
            
            
        return {
            "tutor": {
                "name": self.tutor.get_full_name("cz") if self.tutor else "Zatím bez lektora",
                "id": self.tutor_id,
            },
            "name_cz": self.get_name_cz(),
            "name_en": self.get_name_en(),
            "capacity": "ne" if not self.has_capacity else f"ano: {self.capacity}",
            "secondary_billing_behavior": secondary_billing_behavior,
            "is_time_exclusive": "Ano" if self.is_time_exclusive else "Ne",
            "age_group": age_group,
            "primary_participants": [{"name": u.get_full_name("cz"), "link": "/organizator/detail_ucastnika/" + str(u.id), "cas": pretty_datetime(u.datetime_class_pick), "surname": u.surname or "", "secondary_classes": ", ".join([sc.name_cz for sc in u.secondary_classes]) if u.secondary_classes else "-" } for u in sorted(self.primary_participants, key=lambda u: czech_sort.key(u.surname or ""))],
            "secondary_participants": [{"name": u.get_full_name("cz"), "link": "/organizator/detail_ucastnika/" + str(u.id)} for u in sorted(self.secondary_participants, key=lambda u: czech_sort.key(u.surname or ""))],
            "primary_participants_count": len(self.primary_participants),
            "secondary_participants_count": len(self.secondary_participants),
        }
    
    
    def data_pro_upravu_ucastniku(self):
        return {
            "id": self.id,
            "name": self.get_name_cz()
        }
    
    
    def info_for_admin_edit(self):
        return {
            "name": self.get_name_cz(),
            "discipline_cz": self.discipline_cz,
            "discipline_en": self.discipline_en,
            "has_capacity": "Ano" if self.has_capacity else "Ne",
            "capacity": self.capacity,
            "age_group": self.age_group,
            "secondary_billing_behavior": self.secondary_billing_behavior,
            "is_time_exclusive": "Ano" if self.is_time_exclusive else "Ne",
            "tutor_id": self.tutor_id if self.tutor_id else "-",
        }
        
        
    def nacist_zmeny_z_requestu(self, request):
        self.discipline_cz = request.form.get("discipline_cz")
        self.discipline_en = request.form.get("discipline_en")
        self.has_capacity = request.form.get("has_capacity") == "Ano"
        self.capacity = int(request.form.get("capacity"))
        self.age_group = request.form.get("age_group")
        self.secondary_billing_behavior = request.form.get("secondary_billing_behavior")
        self.is_time_exclusive = request.form.get("is_time_exclusive") == "Ano"
        self.tutor_id = int(request.form.get("tutor_id")) if request.form.get("tutor_id") != "-" else None
        self.update()
        
    
    def data_pro_seznamy(self):
        return {
            "id": self.id,
            "name": self.get_name_cz()
        }
        
        
    def class_capacity_data(self) -> dict:
        state_main = "available" #available, enrolled, full
        if current_user in self.primary_participants:
            state_main = "enrolled"
        elif not self.has_capacity:
            state_main = "available"
        elif len(self.primary_participants) >= self.capacity:
            state_main = "full"
            
        state_secondary = "available" #available, enrolled, full
        if current_user in self.secondary_participants:
            state_secondary = "enrolled"
        elif not self.has_capacity:
            state_secondary = "available"
        elif len(self.secondary_participants) >= self.capacity:
            state_secondary = "full"
            
        state_time_exclusive = "available" #available, enrolled, full
        if current_user in self.secondary_participants: # time exclusive tridy jsou vzdy jako vedlejsi
            state_time_exclusive = "enrolled"
        elif not self.has_capacity:
            state_time_exclusive = "available"
        elif len(self.secondary_participants) >= self.capacity:
            state_time_exclusive = "full"
            
            
            
        return {
            "id": self.id,
            "cz_name": self.get_name_cz(),
            "en_name": self.get_name_en(),
            "capacity": self.capacity,
            "places_taken": len(self.primary_participants) + len(self.secondary_participants),
            "has_capacity": self.has_capacity,
            "state_main": state_main,
            "state_secondary": state_secondary,
            "state_time_exclusive": state_time_exclusive
        }
    
    
    @staticmethod
    def classes_overview():
        result = []
        tridy = sorted(Trida.get_all(), key=lambda t: czech_sort.key(t.get_name_cz() or ""))
        
        def _get_anonymous_user_texts(count: int, has_only_anonymous_participants: bool) -> dict[str, str]:
            # creates texts: Žádní účastníci / Jeden účastník / {2,3,4} účastníci / {5+} účastníků
            # or, "a žádní další účastníci" / "a jeden další účastník" / "a {2,3,4} další účastníci" / "a {5+} dalších účastníků" if has_only_anonymous_participants is False
            # all that in cz and en
            texts = {
                "cz":"",
                "en":""
            }
            if has_only_anonymous_participants:
                if count == 0:
                    texts["cz"] = "Žádní účastníci"
                    texts["en"] = "No participants"
                elif count == 1:
                    texts["cz"] = "Jeden účastník"
                    texts["en"] = "One participant"
                elif count in [2,3,4]:
                    texts["cz"] = f"{count} účastníci"
                    texts["en"] = f"{count} participants"
                else:
                    texts["cz"] = f"{count} účastníků"
                    texts["en"] = f"{count} participants"
            else:
                if count == 0:
                    texts["cz"] = "a žádní další účastníci"
                    texts["en"] = "and no additional participants"
                elif count == 1:
                    texts["cz"] = "a jeden další účastník"
                    texts["en"] = "and one additional participant"
                elif count in [2,3,4]:
                    texts["cz"] = f"a {count} další účastníci"
                    texts["en"] = f"and {count} additional participants"
                else:
                    texts["cz"] = f"a {count} dalších účastníků"
                    texts["en"] = f"and {count} additional participants"
            return texts
        
        for trida in tridy:
            
            main_participants = sorted(trida.primary_participants, key=lambda u: czech_sort.key(u.surname or ""))
            secondary_participants = sorted(trida.secondary_participants, key=lambda u: czech_sort.key(u.surname or ""))
            
            entry = {
                "id": trida.id,
                "name_cz": trida.get_name_cz(),
                "name_en": trida.get_name_en(),
                "main_participants": [],
                "secondary_participants": [],
                "main_participants_anonymous_cz": "",
                "main_participants_anonymous_en": "",
                "secondary_participants_anonymous_cz": "",
                "secondary_participants_anonymous_en": "",
            }
            
            main_participants_anonymous_count = 0
            main_participants_only_anonymous = True
            secondary_participants_anonymous_count = 0
            secondary_participants_only_anonymous = True
            
            for participant in main_participants:
                if participant.show_name_in_class_list:
                    main_participants_only_anonymous = False
                    participant_text = participant.get_full_name("cz")
                    if participant.musical_instrument:
                        participant_text += f" - {participant.musical_instrument}"
                    entry["main_participants"].append(participant_text)
                else:
                    main_participants_anonymous_count += 1
                
            for participant in secondary_participants:
                if participant.show_name_in_class_list:
                    secondary_participants_only_anonymous = False
                    participant_text = participant.get_full_name("cz")
                    if participant.musical_instrument:
                        participant_text += f" - ({participant.musical_instrument})"
                    entry["secondary_participants"].append(participant_text)
                else:
                    secondary_participants_anonymous_count += 1
            
            main_texts = _get_anonymous_user_texts(main_participants_anonymous_count, main_participants_only_anonymous)
            secondary_texts = _get_anonymous_user_texts(secondary_participants_anonymous_count, secondary_participants_only_anonymous)
        
            
            entry["main_participants_anonymous_cz"] = main_texts["cz"]
            entry["main_participants_anonymous_en"] = main_texts["en"]
            entry["secondary_participants_anonymous_cz"] = secondary_texts["cz"]
            entry["secondary_participants_anonymous_en"] = secondary_texts["en"]
            result.append(entry)
            
        return result