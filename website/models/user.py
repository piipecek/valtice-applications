from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from website.models.trida import Trida
from website.helpers.pretty_date import pretty_datetime
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_login import UserMixin, login_user
import jwt
from werkzeug.security import generate_password_hash

#todo procistit stare importy
# from website import db
# from website.models.common_methods_db_model import Common_methods_db_model
# from website.helpers.pretty_date import pretty_datetime
# from datetime import datetime, date
# from flask_login import UserMixin
# from website.models.trida import Trida
# from website.models.cena import Cena
# from io import BytesIO
# from openpyxl import Workbook
# import czech_sort


class User(Common_methods_db_model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # personal data
    name = db.Column(db.String(200))
    surname = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    is_student = db.Column(db.Boolean, default=False)
    
    #automatic data
    datetime_created = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    
    #valtice data
    is_ssh_member = db.Column(db.Boolean, default=False)
    is_active_participant = db.Column(db.Boolean, default=True)
    is_student_of_partner_zus = db.Column(db.Boolean, default=False)
    datetime_registered = db.Column(db.DateTime)
    accomodation_type = db.Column(db.String(200)) # own/vs/gym
    accomodation_count = db.Column(db.Integer, default=0)
    musical_education = db.Column(db.Text)
    musical_instrument = db.Column(db.String(1000))
    repertoire = db.Column(db.Text)
    comment = db.Column(db.Text)
    admin_comment = db.Column(db.Text)
    
    #billing data
    billing_currency = db.Column(db.String(200)) # czk/eur
    billing_email = db.Column(db.String(200))
    billing_age = db.Column(db.String(200)) # child/youth/adult
    billing_date_paid = db.Column(db.Date)
    billing_gift = db.Column(db.Integer, default=0)
    billing_correction = db.Column(db.Integer, default=0)
    billing_correction_reason = db.Column(db.Text)
    billing_food_correction = db.Column(db.Integer, default=0)
    billing_food_correction_reason = db.Column(db.Text)
    billing_accomodation_correction = db.Column(db.Integer, default=0)
    billing_accomodation_correction_reason = db.Column(db.Text)
    
    #tutor data
    
    tutor_travel = db.Column(db.String(200)) #own/public
    tutor_license_plate = db.Column(db.String(200))
    tutor_arrival = db.Column(db.Text)
    tutor_departure = db.Column(db.Text)
    tutor_accompanying_names = db.Column(db.Text)
    tutor_adress = db.Column(db.Text)
    tutor_date_of_birth = db.Column(db.Date)
    tutor_bank_account = db.Column(db.String(200))
    
    #auth data
    password = db.Column(db.String(200))
    must_change_password_upon_login = db.Column(db.Boolean, default=False)
    confirmed_email = db.Column(db.Boolean, default=False)
    
    #relationships
    roles = db.relationship("Role", secondary=user_role_jointable, back_populates="users")
    
    parent_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    parent = db.relationship("User", remote_side=[id], back_populates="children")
    children = db.relationship("User", back_populates="parent")
    
    meal_orders = db.relationship("Meal_order", back_populates="user")
    
    taught_classes = db.relationship("Trida", back_populates="tutor", foreign_keys="Trida.tutor_id")
    main_class_id_priority_1 = db.Column(db.Integer, db.ForeignKey("trida.id"))
    main_class_priority_1 = db.relationship("Trida", back_populates="main_paticipants_priority_1", foreign_keys=[main_class_id_priority_1])
    main_class_id_priority_2 = db.Column(db.Integer, db.ForeignKey("trida.id"))
    main_class_priority_2 = db.relationship("Trida", back_populates="main_paticipants_priority_2", foreign_keys=[main_class_id_priority_2])
    secondary_class_id = db.Column(db.Integer, db.ForeignKey("trida.id"))
    secondary_class = db.relationship("Trida", back_populates="secondary_participants", foreign_keys=[secondary_class_id])

    
    def __repr__(self) -> str:
        return f"Uživatel | {self.email}"
    
    @staticmethod
    def get_by_email(email) -> "User":
        return db.session.scalars(db.select(User).where(User.email == email)).first()
        
        
    def get_reset_token(self, expires_sec=9000) -> str:
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec)
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return reset_token    
    
    
    @staticmethod
    def verify_reset_token(token) -> "User":
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return None
        return User.get_by_id(data["user_id"])
    

    def get_full_name(self) -> str:
        if self.name is None and self.surname is None:
            return "Beze jména"
        return f"{self.name} {self.surname}"
    
    
    def info_pro_seznam(self) -> dict:
        full_name = self.get_full_name()
        return {
            "id": self.id,
            "full_name": full_name if full_name else "-",
            "prijmeni": self.surname if self.surname else "-",
            "email": self.email if self.email else "-",
            "registrovan": "Registrován" if self.datetime_registered else "-",
            "hlavni_trida_1": self.main_class_priority_1.short_name_cz if self.main_class_priority_1 else "-",
            "hlavni_trida_1_id": self.main_class_id_priority_1
        }
    
    
    def info_pro_detail(self):
        def pretty_penize(castka) -> str:
            if castka == 0:
                return "-"
            if castka == int(castka):
                castka = int(castka)
            else:
                castka = str(round(castka, 2)).replace(".", ",")
            if self.billing_currency == "CZK":
                return f"{castka} Kč"
            elif self.finance_mena == "EUR":
                return f"{castka} €"
         
        # ubytovani
        if self.accomodation_type == "own":
            ubytovani = "Vlastní"
        elif self.accomodation_type == "vs":
            ubytovani = "Vinařská škola"
        else:
            ubytovani = "Tělocvična"
        ubytovani = f"{ubytovani}: {self.accomodation_count}"
            

                
        kalkulace = self.kalkulace()
        return {
            "datetime_created": pretty_datetime(self.datetime_created),
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else "Zatím neregistrován",
            #atd, cele prepsat
            # "prijmeni": self.prijmeni,
            # "jmeno": self.jmeno,
            # "vek": self.vek if self.vek else "-",
            # "email": self.email,
            # "telefon": self.telefon if self.telefon else "-",
            # "ssh_clen": "Ano" if self.ssh_clen else "Ne",
            # "ucast": self.ucast,
            # "ubytovani": ubytovani,
            # "strava": "Má zájem, viz. níže" if self.strava else "Nemá zájem",
            # "vzdelani": "-" if not self.vzdelani else self.vzdelani,
            # "nastroj": "-" if not self.nastroj else self.nastroj,
            # "repertoir": "-" if not self.repertoir else self.repertoir,
            # "student_zus_valtice_mikulov": "Ano" if self.student_zus_valtice_mikulov else "Ne",
            # "uzivatelska_poznamka": self.uzivatelska_poznamka if self.uzivatelska_poznamka else "-",
            # "admin_poznamka": self.admin_poznamka if self.admin_poznamka else "-",
            # "hlavni_trida_1": {
            #     "name": Trida.get_by_id(self.hlavni_trida_1_id).full_name if self.hlavni_trida_1_id else "-",
            #     "link": "/organizator/trida/" + str(self.hlavni_trida_1_id) if self.hlavni_trida_1_id else None
            # },
            # "hlavni_trida_2": {
            #     "name": Trida.get_by_id(self.hlavni_trida_2_id).full_name if self.hlavni_trida_2_id else "-",
            #     "link": "/organizator/trida/" + str(self.hlavni_trida_2_id) if self.hlavni_trida_2_id else None
            # },
            # "vedlejsi_trida_placena": {
            #     "name": Trida.get_by_id(self.vedlejsi_trida_placena_id).full_name if self.vedlejsi_trida_placena_id else "-",
            #     "link": "/organizator/trida/" + str(self.vedlejsi_trida_placena_id) if self.vedlejsi_trida_placena_id else None
            # },
            # "vedlejsi_trida_zdarma": {
            #     "name": Trida.get_by_id(self.vedlejsi_trida_zdarma_id).full_name if self.vedlejsi_trida_zdarma_id else "-",
            #     "link": "/organizator/trida/" + str(self.vedlejsi_trida_zdarma_id) if self.vedlejsi_trida_zdarma_id else None
            # },
            # "finance_dne": pretty_datetime(self.finance_dne) if self.finance_dne else "Zatím neplaceno",
            # "finance_celkem": pretty_penize(kalkulace["celkem"]),
            # "finance_trida_1": pretty_penize(kalkulace["prvni_trida"]),
            # "finance_trida_2": pretty_penize(kalkulace["vedlejsi_trida"]),
            # "finance_ubytovani": pretty_penize(kalkulace["ubytovani"]),
            # "finance_snidane": pretty_penize(kalkulace["snidane"]),
            # "finance_obedy": pretty_penize(kalkulace["obedy"]),
            # "finance_vecere": pretty_penize(kalkulace["vecere"]),
            # "finance_dar": pretty_penize(kalkulace["dar"]),
            # "finance_korekce_kurzovne": pretty_penize(self.finance_korekce_kurzovne),
            # "finance_korekce_strava": pretty_penize(self.finance_korekce_strava),
            # "finance_korekce_ubytko": pretty_penize(self.finance_korekce_ubytko),
            # "finance_korekce_kurzovne_duvod": self.finance_korekce_kurzovne_duvod if self.finance_korekce_kurzovne_duvod else "-",
            # "finance_korekce_strava_duvod": self.finance_korekce_strava_duvod if self.finance_korekce_strava_duvod else "-",
            # "finance_korekce_ubytko_duvod": self.finance_korekce_ubytko_duvod if self.finance_korekce_ubytko_duvod else "-",
            # "strava_snidane": snidane,
            # "strava_obedy": obed,
            # "strava_vecere": vecere,
            # "strava_na_ocich": strava_na_ocich,
        }
    
    
    
    @staticmethod
    def get_seznam_pro_udileni_roli() -> list:
        result = []
        for u in User.get_all():
            data = {
                "id": u.id,
                "email": u.email,
                "role": ", ".join([r.display_name for r in sorted(u.roles)])
            }
            result.append(data)
        return result
    
    
    def login(self):
        login_user(self, remember=True)
        self.update()
        
        
    def get_info_pro_seznam_useru(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
        }

        
    @staticmethod
    def novy_ucet_from_admin(email, password) -> int:
        if User.get_by_email(email):
            return None
        u = User()
        u.email = email
        u.password = generate_password_hash(password, method="scrypt")
        u.confirmed_email = True
        u.update()
        return u.id
    
    #todo prepsat stare funckce
    
    # def kalkulace(self) -> dict:
    #     # ubytovani
    #     if self.ubytovani in ["Tělocvična", "Tělocvična (náhradník)"]:
    #         if self.finance_mena == "CZK":        
    #             ubytko = self.ubytovani_pocet * Cena.get_by_system_name("telocvicna").czk
    #         elif self.finance_mena == "EUR":
    #             ubytko = self.ubytovani_pocet * Cena.get_by_system_name("telocvicna").eur
    #     elif self.ubytovani == "Internát vinařské školy":
    #         if self.finance_mena == "CZK":
    #             ubytko = self.ubytovani_pocet * Cena.get_by_system_name("internat").czk
    #         elif self.finance_mena == "EUR":
    #             ubytko = self.ubytovani_pocet * Cena.get_by_system_name("internat").eur
    #     else:
    #         ubytko = 0
        
    #     # kurzovne
    #     def vycislit(ucast: str, mena: str, kategorie: str, clen_ssh: bool, cislo_tridy: int, trida: Trida) -> int:
    #         if trida is None:
    #             return 0
    #         if cislo_tridy == 1:
    #             if ucast == "Pasivní":
    #                 if mena == "CZK":
    #                     return Cena.get_by_system_name("kurzovne_pasivni").czk
    #                 elif mena == "EUR":
    #                     return Cena.get_by_system_name("kurzovne_pasivni").eur
    #             if kategorie == "dite":
    #                 if mena == "CZK":
    #                     return Cena.get_by_system_name("kurzovne_deti").czk
    #                 elif mena == "EUR":
    #                     return Cena.get_by_system_name("kurzovne_deti").eur
    #             elif kategorie == "student":
    #                 if mena == "CZK":
    #                     return Cena.get_by_system_name("kurzovne_student").czk
    #                 elif mena == "EUR":
    #                     return Cena.get_by_system_name("kurzovne_student").eur
    #             elif clen_ssh:
    #                 if mena == "CZK":
    #                     return Cena.get_by_system_name("kurzovne_ssh").czk
    #                 elif mena == "EUR":
    #                     return Cena.get_by_system_name("kurzovne_ssh").eur
    #             elif kategorie == "dospely":
    #                 if mena == "CZK":
    #                     return Cena.get_by_system_name("kurzovne").czk
    #                 elif mena == "EUR":
    #                     return Cena.get_by_system_name("kurzovne").eur
    #         elif cislo_tridy == 2:
    #             if trida.je_zdarma_jako_vedlejsi:
    #                 return 0
    #             elif trida.je_ansamblova:
    #                 if mena == "CZK":
    #                     return Cena.get_by_system_name("ansambly").czk
    #                 elif mena == "EUR":
    #                     return Cena.get_by_system_name("ansambly").eur
    #             else:
    #                 return vycislit(ucast, mena, kategorie, clen_ssh, 1, trida)
        
    #     prvni_trida = vycislit(self.ucast, self.finance_mena, self.finance_kategorie, self.ssh_clen, 1, self.hlavni_trida_1)
    #     vedlejsi_trida_placena = vycislit(self.ucast, self.finance_mena, self.finance_kategorie, self.ssh_clen, 2, self.vedlejsi_trida_placena)
        
        
    #     # strava
    #     if self.finance_mena == "CZK":
    #         snidane = self.strava_snidane_zs * Cena.get_by_system_name("snidane_zs").czk + self.strava_snidane_vinarska * Cena.get_by_system_name("snidane_ss").czk
    #         obedy = self.strava_obed_zs_maso * Cena.get_by_system_name("obed_zs").czk + self.strava_obed_zs_vege * Cena.get_by_system_name("obed_zs").czk + self.strava_obed_vinarska_maso * Cena.get_by_system_name("obed_ss").czk + self.strava_obed_vinarska_vege * Cena.get_by_system_name("obed_ss").czk
    #         vecere = self.strava_vecere_zs_maso * Cena.get_by_system_name("vecere_zs").czk + self.strava_vecere_zs_vege * Cena.get_by_system_name("vecere_zs").czk + self.strava_vecere_vinarska_maso * Cena.get_by_system_name("vecere_ss").czk + self.strava_vecere_vinarska_vege * Cena.get_by_system_name("vecere_ss").czk
    #     elif self.finance_mena == "EUR":
    #         snidane = self.strava_snidane_zs * Cena.get_by_system_name("snidane_zs").eur + self.strava_snidane_vinarska * Cena.get_by_system_name("snidane_ss").eur
    #         obedy = self.strava_obed_zs_maso * Cena.get_by_system_name("obed_zs").eur + self.strava_obed_zs_vege * Cena.get_by_system_name("obed_zs").eur + self.strava_obed_vinarska_maso * Cena.get_by_system_name("obed_ss").eur + self.strava_obed_vinarska_vege * Cena.get_by_system_name("obed_ss").eur
    #         vecere = self.strava_vecere_zs_maso * Cena.get_by_system_name("vecere_zs").eur + self.strava_vecere_zs_vege * Cena.get_by_system_name("vecere_zs").eur + self.strava_vecere_vinarska_maso * Cena.get_by_system_name("vecere_ss").eur + self.strava_vecere_vinarska_vege * Cena.get_by_system_name("vecere_ss").eur
        
    #     result = {
    #         "ubytovani": ubytko,
    #         "prvni_trida": prvni_trida,
    #         "vedlejsi_trida": vedlejsi_trida_placena,
    #         "snidane": snidane,
    #         "obedy": obedy,
    #         "vecere": vecere,
    #         "dar": self.finance_dar,
    #         "celkem": ubytko + snidane + obedy + vecere + self.finance_dar + prvni_trida + vedlejsi_trida_placena + self.finance_korekce_kurzovne + self.finance_korekce_strava + self.finance_korekce_ubytko
    #     }
    #     return result
    
    
    def info_pro_upravu(self):
        return {
            "name": self.name if self.name else "",
            "surname": self.surname if self.surname else "",
            "email": self.email,
            "phone": self.phone,
            "is_student": "Ano" if self.is_student else "Ne",
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "active" if self.is_active_participant else "passive",
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else None,
            "accomodation_type": self.accomodation_type,
            "accomodation_count": self.accomodation_count,
            "musical_education": self.musical_education,
            "musical_instrument": self.musical_instrument,
            "repertoire": self.repertoire,
            "comment": self.comment,
            "admin_comment": self.admin_comment,
            
            "billing_currency": self.billing_currency,
            "billing_email": self.billing_email,
            "billing_age": self.billing_age,
            "billing_date_paid": pretty_datetime(self.billing_date_paid) if self.billing_date_paid else None,
            "billing_correction": self.billing_correction,
            "billing_correction_reason": self.billing_correction_reason,
            "billing_food_correction": self.billing_food_correction,
            "billing_food_correction_reason": self.billing_food_correction_reason,
            "billing_accomodation_correction": self.billing_accomodation_correction,
            "billing_accomodation_correction_reason": self.billing_accomodation_correction_reason,
            "billing_gift": self.billing_gift,
            
            "tutor_travel": self.tutor_travel,
            "tutor_license_plate": self.tutor_license_plate,
            "tutor_arrival": self.tutor_arrival,
            "tutor_departure": self.tutor_departure,
            "tutor_accompanying_names": self.tutor_accompanying_names,
            "tutor_adress": self.tutor_adress,
            "tutor_date_of_birth": self.tutor_date_of_birth,
            "tutor_bank_account": self.tutor_bank_account,
            
            "must_change_password_upon_login": "Ano" if self.must_change_password_upon_login else "Ne",
            "confirmed_email": "Ano" if self.confirmed_email else "Ne",
            
            "main_class_id_priority_1": self.main_class_priority_1.id if self.main_class_priority_1 else None,
            "main_class_id_priority_2": self.main_class_priority_2.id if self.main_class_priority_2 else None,
            "secondary_class_id": self.secondary_class.id if self.secondary_class else None,
            #TODO tady určitě přibudou meals a children
        }
    
    # def nacist_zmeny_z_requestu(self, request):
    #     self.jmeno = request.form.get("jmeno")
    #     self.prijmeni = request.form.get("prijmeni")
    #     self.vek = request.form.get("vek")
    #     self.email = request.form.get("email")
    #     self.telefon = request.form.get("telefon")
    #     self.finance_dne = datetime.strptime(request.form.get("finance_dne"), "%Y-%m-%d") if request.form.get("finance_dne") else None
    #     self.finance_dar = float(request.form.get("finance_dar"))
    #     self.finance_mena = request.form.get("finance_mena")
    #     self.finance_kategorie = request.form.get("finance_kategorie")
    #     self.finance_korekce_kurzovne = float(request.form.get("finance_korekce_kurzovne"))
    #     self.finance_korekce_kurzovne_duvod = request.form.get("finance_korekce_kurzovne_duvod")
    #     self.finance_korekce_strava = float(request.form.get("finance_korekce_strava"))
    #     self.finance_korekce_strava_duvod = request.form.get("finance_korekce_strava_duvod")
    #     self.finance_korekce_ubytko = float(request.form.get("finance_korekce_ubytko"))
    #     self.finance_korekce_ubytko_duvod = request.form.get("finance_korekce_ubytko_duvod")
    #     self.ssh_clen = True if request.form.get("ssh_clen") == "Ano" else False
    #     self.ucast = request.form.get("ucast")
    #     self.hlavni_trida_1_id = int(request.form.get("hlavni_trida_1")) if request.form.get("hlavni_trida_1") != "-" else None
    #     self.hlavni_trida_2_id = int(request.form.get("hlavni_trida_2")) if request.form.get("hlavni_trida_2") != "-" else None
    #     self.vedlejsi_trida_placena_id = int(request.form.get("vedlejsi_trida_placena")) if request.form.get("vedlejsi_trida_placena") != "-" else None
    #     self.vedlejsi_trida_zdarma_id = int(request.form.get("vedlejsi_trida_zdarma")) if request.form.get("vedlejsi_trida_zdarma") != "-" else None
    #     self.ubytovani = request.form.get("ubytovani")
    #     self.ubytovani_pocet = float(request.form.get("ubytovani_pocet"))
    #     self.vzdelani = request.form.get("vzdelani")
    #     self.nastroj = request.form.get("nastroj")
    #     self.repertoir = request.form.get("repertoir")
    #     self.student_zus_valtice_mikulov = True if request.form.get("student_zus_valtice_mikulov") == "Ano" else False
    #     self.strava = True if request.form.get("strava") == "Ano" else False
    #     self.strava_snidane_vinarska = int(request.form.get("strava_snidane_vinarska")) if request.form.get("strava_snidane_vinarska") else 0
    #     self.strava_snidane_zs = int(request.form.get("strava_snidane_zs")) if request.form.get("strava_snidane_zs") else 0
    #     self.strava_obed_vinarska_maso = int(request.form.get("strava_obed_vinarska_maso")) if request.form.get("strava_obed_vinarska_maso") else 0
    #     self.strava_obed_vinarska_vege = int(request.form.get("strava_obed_vinarska_vege")) if request.form.get("strava_obed_vinarska_vege") else 0
    #     self.strava_obed_zs_maso = int(request.form.get("strava_obed_zs_maso")) if request.form.get("strava_obed_zs_maso") else 0
    #     self.strava_obed_zs_vege = int(request.form.get("strava_obed_zs_vege")) if request.form.get("strava_obed_zs_vege") else 0
    #     self.strava_vecere_vinarska_maso = int(request.form.get("strava_vecere_vinarska_maso")) if request.form.get("strava_vecere_vinarska_maso") else 0
    #     self.strava_vecere_vinarska_vege = int(request.form.get("strava_vecere_vinarska_vege")) if request.form.get("strava_vecere_vinarska_vege") else 0
    #     self.strava_vecere_zs_maso = int(request.form.get("strava_vecere_zs_maso")) if request.form.get("strava_vecere_zs_maso") else 0
    #     self.strava_vecere_zs_vege = int(request.form.get("strava_vecere_zs_vege")) if request.form.get("strava_vecere_zs_vege") else 0
    #     self.uzivatelska_poznamka = request.form.get("uzivatelska_poznamka")
    #     self.admin_poznamka = request.form.get("admin_poznamka")
    #     self.update()
    
    
    # @staticmethod
    # def vytvorit_seznam(kriteria: dict) -> dict:
    #     ucastnici = User.get_all()
        
    #     # filtr tříd
    #     if len(kriteria["tridy"]) != 0:
    #         ucastnici = list(filter(lambda u: u.hlavni_trida_1_id in kriteria["tridy"] or u.hlavni_trida_2_id in kriteria["tridy"] or u.vedlejsi_trida_placena_id in kriteria["tridy"] or u.vedlejsi_trida_zdarma_id in kriteria["tridy"], ucastnici))
        
    #     #filtr ubytka
    #     if len(kriteria["ubytko"]) != 0:
    #         ucastnici = list(filter(lambda u: u.ubytovani in kriteria["ubytko"], ucastnici))
            
    #     # filtr stravy
    #     if len(kriteria["strava"]) != 0:
    #         u_snidane_zs = []
    #         u_snidane_vs = []
    #         u_obed_zs = []
    #         u_obed_vs = []
    #         u_vecere_zs = []
    #         u_vecere_vs = []
    #         if "snidane_zs" in kriteria["strava"]:
    #             u_snidane_zs = list(filter(lambda u: u.strava_snidane_zs > 0, ucastnici))
    #         if "snidane_vs" in kriteria["strava"]:
    #             u_snidane_vs = list(filter(lambda u: u.strava_snidane_vinarska > 0, ucastnici))
    #         if "obed_zs" in kriteria["strava"]:
    #             u_obed_zs = list(filter(lambda u: u.strava_obed_zs_maso + u.strava_obed_zs_vege > 0, ucastnici))
    #         if "obed_vs" in kriteria["strava"]:
    #             u_obed_vs = list(filter(lambda u: u.strava_obed_vinarska_maso + u.strava_obed_vinarska_vege > 0, ucastnici))
    #         if "vecere_zs" in kriteria["strava"]:
    #             u_vecere_zs = list(filter(lambda u: u.strava_vecere_zs_maso + u.strava_vecere_zs_vege > 0, ucastnici))
    #         if "vecere_vs" in kriteria["strava"]:
    #             u_vecere_vs = list(filter(lambda u: u.strava_vecere_vinarska_maso + u.strava_vecere_vinarska_vege > 0, ucastnici))
    #         ucastnici = list(set(u_snidane_zs + u_snidane_vs + u_obed_zs + u_obed_vs + u_vecere_zs + u_vecere_vs))
        
    #     # filtr ostatnich
    #     if "korekce" in kriteria["ostatni"]:
    #         ucastnici = list(filter(lambda u: u.finance_korekce_kurzovne + u.finance_korekce_strava + u.finance_korekce_ubytko != 0, ucastnici))
    #     if "neregistrace" in kriteria["ostatni"]:
    #         ucastnici = list(filter(lambda u: not u.cas_registrace, ucastnici))
    #     if "dar" in kriteria["ostatni"]:
    #         ucastnici = list(filter(lambda u: u.finance_dar != 0, ucastnici))
    #     if "poznamka" in kriteria["ostatni"]:
    #         ucastnici = list(filter(lambda u: u.uzivatelska_poznamka, ucastnici))
        
    #     # serazeni
    #     ucastnici = sorted(ucastnici, key=lambda u: czech_sort.key(u.prijmeni + u.jmeno))
    #     if kriteria["atribut_razeni"] == "prijmeni":
    #         ucastnici = sorted(ucastnici, key=lambda u: czech_sort.key(u.prijmeni))
    #     elif kriteria["atribut_razeni"] == "jmeno":
    #         ucastnici = sorted(ucastnici, key=lambda u: czech_sort.key(u.jmeno))
    #     elif kriteria["atribut_razeni"] == "cas":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.cas)
    #     elif kriteria["atribut_razeni"] == "cas_registrace":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.cas_registrace if u.cas_registrace else datetime(1, 1, 1))
    #     elif kriteria["atribut_razeni"] == "vek":
    #         ucastnici = sorted(ucastnici, key=lambda u: int(u.vek) if u.vek else 0)
    #     elif kriteria["atribut_razeni"] == "finance_dne":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.finance_dne if u.finance_dne else date(1, 1, 1))
    #     elif kriteria["atribut_razeni"] == "finance_dar":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.finance_dar)
    #     elif kriteria["atribut_razeni"] == "finance_celkem":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.kalkulace()["celkem"])
    #     elif kriteria["atribut_razeni"] == "finance_mena":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.finance_mena)
    #     elif kriteria["atribut_razeni"] == "finance_kategorie":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.finance_kategorie)
    #     elif kriteria["atribut_razeni"] == "ssh_clen":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.ssh_clen)
    #     elif kriteria["atribut_razeni"] == "ucast":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.ucast)
    #     elif kriteria["atribut_razeni"] == "ubytovani":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.ubytovani)
    #     elif kriteria["atribut_razeni"] == "student_zus_valtice_mikulov":
    #         ucastnici = sorted(ucastnici, key=lambda u: u.student_zus_valtice_mikulov)

        
    #     # vypsani atribut
    #     result = {
    #         "emaily":"",
    #         "lidi": []
    #     }
    #     for i, u in enumerate(ucastnici):
    #         entry = {
    #             "#": i+1,
    #             "Jméno": f"{u.prijmeni}, {u.jmeno}",
    #         }
    #         for a in kriteria["atributy"]:
    #             if a == "cas":
    #                 entry["Čas vyplnění přihlášky"] = pretty_datetime(u.cas)
    #             elif a == "vek":
    #                 entry["Věk"] = u.vek
    #             elif a == "email":
    #                 entry["Email"] = u.email
    #             elif a == "telefon":
    #                 entry["Telefon"] = u.telefon
    #             elif a == "finance_dne":
    #                 entry["Datum platby"] = pretty_datetime(u.finance_dne)
    #             elif a == "finance_dar":
    #                 entry["Dar"] = u.finance_dar
    #             elif a == "finance_celkem":
    #                 entry["Celkem"] = u.kalkulace()["celkem"]
    #             elif a == "finance_mena":
    #                 entry["Měna"] = u.finance_mena
    #             elif a == "finance_kategorie":
    #                 entry["Kategorie"] = "Dítě" if u.finance_kategorie == "dite" else "Student" if u.finance_kategorie == "student" else "Dospělý"
    #             elif a == "finance_kurzovne":
    #                 entry["Kurzovné"] = u.kalkulace()["prvni_trida"] + u.kalkulace()["vedlejsi_trida"]
    #             elif a == "finance_ubytovani":
    #                 entry["Ubytování"] = u.kalkulace()["ubytovani"]
    #             elif a == "finance_strava":
    #                 entry["strava"] = u.kalkulace()["snidane"] + u.kalkulace()["obedy"] + u.kalkulace()["vecere"]
    #             elif a == "finance_korekce_kurzovne":
    #                 entry["Korekce kurzovné"] = u.finance_korekce_kurzovne
    #             elif a == "finance_korekce_kurzovne_duvod":
    #                 entry["Důvod korekce kurzovné"] = u.finance_korekce_kurzovne_duvod
    #             elif a == "finance_korekce_strava":
    #                 entry["Korekce stravy"] = u.finance_korekce_strava
    #             elif a == "finance_korekce_strava_duvod":
    #                 entry["Důvod korekce stravy"] = u.finance_korekce_strava_duvod
    #             elif a == "finance_korekce_ubytko":
    #                 entry["Korekce ubytování"] = u.finance_korekce_ubytko
    #             elif a == "finance_korekce_ubytko_duvod":
    #                 entry["Důvod korekce ubytování"] = u.finance_korekce_ubytko_duvod
    #             elif a == "ssh_clen":
    #                 entry["Člen SSH"] = "Ano" if u.ssh_clen else "Ne"
    #             elif a == "ucast":
    #                 entry["Účast"] = u.ucast
    #             elif a == "hlavni_trida_1_id":
    #                 entry["Hlavní třída"] = u.hlavni_trida_1.full_name if u.hlavni_trida_1_id else "-"
    #             elif a == "hlavni_trida_2_id":
    #                 entry["Hlavní třída druhá volba"] = u.hlavni_trida_2.full_name if u.hlavni_trida_2_id else "-"
    #             elif a == "vedlejsi_trida_placena_id":
    #                 entry["Vedlejší třída placená"] = u.vedlejsi_trida_placena.full_name if u.vedlejsi_trida_placena_id else "-"
    #             elif a == "vedlejsi_trida_zdarma_id":
    #                 entry["Vedlejší třída zdarma"] = u.vedlejsi_trida_zdarma.full_name if u.vedlejsi_trida_zdarma_id else "-"
    #             elif a == "ubytovani":
    #                 entry["Ubytování"] = u.ubytovani
    #             elif a == "ubytovani_pocet":
    #                 entry["Počet lůžek"] = u.ubytovani_pocet
    #             elif a == "vzdelani":
    #                 entry["Vzdělání"] = u.vzdelani
    #             elif a == "nastroj":
    #                 entry["Nástroj"] = u.nastroj
    #             elif a == "repertoir":
    #                 entry["Repertoár"] = u.repertoir
    #             elif a == "student_zus_valtice_mikulov":
    #                 entry["Student ZUŠ Valtice Mikulov"] = "Ano" if u.student_zus_valtice_mikulov else "Ne"
    #             elif a == "strava":
    #                 entry["Strava"] = u.info_pro_detail()["strava_na_ocich"]
    #             elif a == "uzivatelska_poznamka":
    #                 entry["Uživatelská poznámka"] = u.uzivatelska_poznamka
    #             elif a == "admin_poznamka":
    #                 entry["Admin poznámka"] = u.admin_poznamka
    #             elif a == "cas_registrace":
    #                 entry["Čas registrace"] = pretty_datetime(u.cas_registrace) if u.cas_registrace else "Zatím neregistrován"   
    #         result["lidi"].append(entry)
    #     seen = set()
    #     ordered_unique_emails = []
    #     for u in ucastnici:
    #         if u.email not in seen:
    #             ordered_unique_emails.append(u.email)
    #             seen.add(u.email)

    #     result["emaily"] = ", ".join(ordered_unique_emails)
    #     return result

    # def vytvorit_xlsx_seznam(kriteria) -> BytesIO:
    #     data = User.vytvorit_seznam(kriteria)
    #     wb = Workbook()
    #     ws = wb.active
    #     ws.title = "Učastníci"
    #     keys = data["lidi"][0].keys()
    #     ws.append(list(keys))
    #     for radek in data["lidi"]:
    #         ws.append([radek[k] for k in keys])
    #     output = BytesIO()
    #     wb.save(output)
    #     output.seek(0)
    #     return output