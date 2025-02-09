from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from website.models.trida import Trida
from website.models.billing import Billing
from website.models.role import Role
from website.helpers.pretty_date import pretty_datetime
from website.helpers.pretty_penize import pretty_penize
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_login import UserMixin, login_user
import jwt
from werkzeug.security import generate_password_hash


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
    datetime_class_pick = db.Column(db.DateTime) # udrzuje datum picknuti hlavni tridy priority 1
    datetime_registered = db.Column(db.DateTime)
    accomodation_type = db.Column(db.String(200), default="own") # own/vs/gym
    accomodation_count = db.Column(db.Integer, default=0)
    musical_education = db.Column(db.Text)
    musical_instrument = db.Column(db.String(1000))
    repertoire = db.Column(db.Text)
    comment = db.Column(db.Text)
    admin_comment = db.Column(db.Text)
    
    #billing data
    billing_currency = db.Column(db.String(200), default="czk" ) # czk/eur
    billing_email = db.Column(db.String(200))
    billing_age = db.Column(db.String(200), default="adult") # child/youth/adult
    billing_date_paid = db.Column(db.Date)
    billing_gift = db.Column(db.Integer, default=0)
    billing_correction = db.Column(db.Integer, default=0)
    billing_correction_reason = db.Column(db.Text)
    billing_food_correction = db.Column(db.Integer, default=0)
    billing_food_correction_reason = db.Column(db.Text)
    billing_accomodation_correction = db.Column(db.Integer, default=0)
    billing_accomodation_correction_reason = db.Column(db.Text)
    
    #tutor data
    
    tutor_travel = db.Column(db.String(200), default="own") #own/public
    tutor_license_plate = db.Column(db.String(200))
    tutor_arrival = db.Column(db.Text)
    tutor_departure = db.Column(db.Text)
    tutor_accompanying_names = db.Column(db.Text)
    tutor_address = db.Column(db.Text)
    tutor_date_of_birth = db.Column(db.Date)
    tutor_bank_account = db.Column(db.String(200))
    
    #auth data
    password = db.Column(db.String(200))
    must_change_password_upon_login = db.Column(db.Boolean, default=False)
    confirmed_email = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    
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
        elif f"{self.name} {self.surname}".strip() == "":
            return "Beze jména"
        return f"{self.name} {self.surname}"
    
    
    def info_pro_seznam(self) -> dict:
        full_name = self.get_full_name()
        return {
            "id": self.id,
            "full_name": full_name if full_name else "-",
            "surname": self.surname if self.surname else "-",
            "email": self.email if self.email else "-",
            "registrovan": "Registrován" if self.datetime_registered else "-",
            "hlavni_trida_1": self.main_class_priority_1.short_name_cz if self.main_class_priority_1 else "-",
            "hlavni_trida_1_id": self.main_class_id_priority_1
        }
    
    def info_pro_seznam_lektoru(self) -> dict:
        full_name = self.get_full_name()
        return {
            "id": self.id,
            "full_name": full_name if full_name else "-",
            "surname": self.surname if self.surname else "-",
            "phone": self.phone if self.phone else "-",
            "taught_classes":[
                {
                    "id": trida.id,
                    "short_name": trida.short_name_cz
                } for trida in self.taught_classes
            ],
        }
        
    @staticmethod
    def get_seznam_pro_udileni_roli() -> list:
        result = []
        for u in User.get_all():
            data = {
                "id": u.id,
                "email": u.email,
                "role": ", ".join([r.display_name for r in sorted(u.roles)]),
                "name": u.get_full_name()
            }
            result.append(data)
        return result

    @staticmethod
    def get_seznam_pro_options_na_uprave_tridy() -> list:
        result = []
        tutor_role = Role.get_by_system_name("tutor")
        for u in User.get_all():
            if tutor_role in u.roles:
                data = {
                    "id": u.id,
                    "full_name": u.get_full_name(),
                    "surname": u.surname
                }
                result.append(data)
        return sorted(result, key=lambda x: (x["surname"] is None, x["surname"] or ""))
    
    
    def login(self):
        login_user(self, remember=True)
        self.update()
        
        
    def get_info_pro_seznam_useru(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
        }
    
    
    def kalkulace(self) -> dict:
        # ubytovani
        if self.accomodation_type == "gym":
            if self.billing_currency == "czk":      
                ubytko = self.accomodation_count * Billing.get_by_system_name("telocvicna").czk
            elif self.billing_currency == "eur":
                ubytko = self.accomodation_count * Billing.get_by_system_name("telocvicna").eur
        elif self.accomodation_type == "vs":
            if self.billing_currency == "czk":
                ubytko = self.accomodation_count * Billing.get_by_system_name("internat").czk
            elif self.billing_currency == "eur":
                ubytko = self.accomodation_count * Billing.get_by_system_name("internat").eur
        else:
            ubytko = None
        
        # kurzovne
        def calculate_trida(trida: Trida, self, je_vedlejsi) -> int:
            if trida is None:
                return None
            if not self.is_active_participant: # pasivní účastníci
                if self.billing_currency == "czk":
                    return Billing.get_by_system_name("kurzovne_pasivni").czk
                elif self.billing_currency == "eur":
                    return Billing.get_by_system_name("kurzovne_pasivni").eur
            if je_vedlejsi:
                if trida.is_free_as_secondary: # napr. zapsanej sbor jako vedlejsi trida
                    return 0
                elif not trida.is_solo: # napr. zapsana Poppy Holden jako vedlejsi trida
                    if self.billing_currency == "czk":
                        return Billing.get_by_system_name("ansambly").czk
                    elif self.billing_currency == "eur":
                        return Billing.get_by_system_name("ansambly").eur
                else:
                    return calculate_trida(trida, self, False) # napr. zapsana solo trida jako vedlejsi trida, pocita se to znova aby byly slevy apod.
            else:
                if self.billing_age == "child":
                    if self.billing_currency == "czk":
                        return Billing.get_by_system_name("kurzovne_deti").czk
                    elif self.billing_currency == "eur":
                        return Billing.get_by_system_name("kurzovne_deti").eur
                elif self.billing_age == "youth":
                    if self.billing_currency == "czk":
                        return Billing.get_by_system_name("kurzovne_deti").czk
                    elif self.billing_currency == "eur":
                        return Billing.get_by_system_name("kurzovne_deti").eur
                elif self.is_ssh_member:
                    if self.billing_currency == "czk":
                        return Billing.get_by_system_name("kurzovne_ssh").czk
                    elif self.billing_currency == "eur":
                        return Billing.get_by_system_name("kurzovne_ssh").eur
                elif self.is_student:
                    if self.billing_currency == "czk":
                        return Billing.get_by_system_name("kurzovne_student").czk
                    elif self.billing_currency == "eur":
                        return Billing.get_by_system_name("kurzovne_student").eur
                else:
                    if self.billing_currency == "czk":
                        return Billing.get_by_system_name("kurzovne").czk
                    elif self.billing_currency == "eur":
                        return Billing.get_by_system_name("kurzovne").eur
                
        
        hlavni_trida = calculate_trida(self.main_class_priority_1, self, False)
        vedlejsi_trida = calculate_trida(self.secondary_class, self, True)
        
        
        # # strava
        #TODO strava jinak
        # if self.finance_mena == "CZK":
        #     snidane = self.strava_snidane_zs * Billing.get_by_system_name("snidane_zs").czk + self.strava_snidane_vinarska * Billing.get_by_system_name("snidane_ss").czk
        #     obedy = self.strava_obed_zs_maso * Billing.get_by_system_name("obed_zs").czk + self.strava_obed_zs_vege * Billing.get_by_system_name("obed_zs").czk + self.strava_obed_vinarska_maso * Billing.get_by_system_name("obed_ss").czk + self.strava_obed_vinarska_vege * Billing.get_by_system_name("obed_ss").czk
        #     vecere = self.strava_vecere_zs_maso * Billing.get_by_system_name("vecere_zs").czk + self.strava_vecere_zs_vege * Billing.get_by_system_name("vecere_zs").czk + self.strava_vecere_vinarska_maso * Billing.get_by_system_name("vecere_ss").czk + self.strava_vecere_vinarska_vege * Billing.get_by_system_name("vecere_ss").czk
        # elif self.finance_mena == "EUR":
        #     snidane = self.strava_snidane_zs * Billing.get_by_system_name("snidane_zs").eur + self.strava_snidane_vinarska * Billing.get_by_system_name("snidane_ss").eur
        #     obedy = self.strava_obed_zs_maso * Billing.get_by_system_name("obed_zs").eur + self.strava_obed_zs_vege * Billing.get_by_system_name("obed_zs").eur + self.strava_obed_vinarska_maso * Billing.get_by_system_name("obed_ss").eur + self.strava_obed_vinarska_vege * Billing.get_by_system_name("obed_ss").eur
        #     vecere = self.strava_vecere_zs_maso * Billing.get_by_system_name("vecere_zs").eur + self.strava_vecere_zs_vege * Billing.get_by_system_name("vecere_zs").eur + self.strava_vecere_vinarska_maso * Billing.get_by_system_name("vecere_ss").eur + self.strava_vecere_vinarska_vege * Billing.get_by_system_name("vecere_ss").eur
        snidane = 11
        obedy = 22
        vecere = 33
        
        hlavni_trida_do_sumy = hlavni_trida if hlavni_trida is not None else 0
        vedlejsi_trida_do_sumy = vedlejsi_trida if vedlejsi_trida is not None else 0
        ubytko_do_sumy = ubytko if ubytko is not None else 0
        result = {
            "ubytovani": ubytko,
            "prvni_trida": hlavni_trida,
            "vedlejsi_trida": vedlejsi_trida,
            "snidane": snidane,
            "obedy": obedy,
            "vecere": vecere,
            "dar": self.billing_gift,
            "celkem": ubytko_do_sumy + snidane + obedy + vecere + self.billing_gift + hlavni_trida_do_sumy + vedlejsi_trida_do_sumy + self.billing_correction + self.billing_food_correction + self.billing_accomodation_correction
        }
        return result
    
    
    def info_pro_detail(self):
        # ubytovani
        if self.accomodation_type == "own":
            ubytovani = "vlastní"
        elif self.accomodation_type == "vs":
            ubytovani = f"vinařská škola: {self.accomodation_count}"
        else:
            ubytovani = f"tělocvična: {self.accomodation_count}"
            
        # billing kategorie
        if self.billing_age == "child":
            billing_age = "dítě"
        elif self.billing_age == "youth":
            billing_age = "mládež do 15 let"
        else:
            billing_age = "dospělý"
            
        billing_email = self.billing_email if self.billing_email else "bude použit hlavní e-mail"
        if self.parent:
            billing_email = "bude použit e-mail rodiče"

                
        kalkulace = self.kalkulace()
        return {
            "name": self.name if self.name else "-",
            "surname": self.surname if self.surname else "-",
            "full_name": self.get_full_name(),
            "email": self.email,
            "phone": self.phone if self.phone else "-",
            "is_student": "Ano" if self.is_student else "Ne",
            "datetime_class_pick": pretty_datetime(self.datetime_class_pick) if self.datetime_class_pick else "Zatím nevybráno",
            "datetime_created": pretty_datetime(self.datetime_created),
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "aktivní" if self.is_active_participant else "pasivní",
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else "Zatím neregistrován",
            "accomodation_type": ubytovani,
            "musical_education": self.musical_education if self.musical_education else "-",
            "musical_instrument": self.musical_instrument if self.musical_instrument else "-",
            "repertoire": self.repertoire if self.repertoire else "-",
            "comment": self.comment if self.comment else "-",
            "admin_comment": self.admin_comment if self.admin_comment else "-",
            "billing_email": billing_email,
            "billing_age": billing_age,
            "billing_date_paid": pretty_datetime(self.billing_date_paid) if self.billing_date_paid else "Zatím neplaceno",
            "billing_correction": pretty_penize(self.billing_correction, self.billing_currency),
            "billing_correction_reason": self.billing_correction_reason if self.billing_correction_reason else "-",
            "billing_food_correction": pretty_penize(self.billing_food_correction, self.billing_currency),
            "billing_food_correction_reason": self.billing_food_correction_reason if self.billing_food_correction_reason else "-",
            "billing_accomodation_correction": pretty_penize(self.billing_accomodation_correction, self.billing_currency),
            "billing_accomodation_correction_reason": self.billing_accomodation_correction_reason if self.billing_accomodation_correction_reason else "-",
            "is_tutor": True if Role.get_by_system_name("tutor") in self.roles else False,
            "taught_classes":[
                {
                    "id": trida.id,
                    "short_name": trida.short_name_cz
                } for trida in self.taught_classes
            ],
            "tutor_travel": "vlastní" if self.tutor_travel == "own" else "veřejná",
            "tutor_license_plate": self.tutor_license_plate if self.tutor_license_plate else "-",
            "tutor_arrival": self.tutor_arrival if self.tutor_arrival else "-",
            "tutor_departure": self.tutor_departure if self.tutor_departure else "-",
            "tutor_accompanying_names": self.tutor_accompanying_names if self.tutor_accompanying_names else "-",
            "tutor_address": self.tutor_address if self.tutor_address else "-",
            "tutor_date_of_birth": pretty_datetime(self.tutor_date_of_birth) if self.tutor_date_of_birth else "-",
            "tutor_bank_account": self.tutor_bank_account if self.tutor_bank_account else "-",
            "must_change_password_upon_login": "Ano" if self.must_change_password_upon_login else "Ne",
            "confirmed_email": "Ano" if self.confirmed_email else "Ne",
            "is_locked": "Ano" if self.is_locked else "Ne",
            "roles": ", ".join([r.display_name for r in sorted(self.roles)]) if self.roles else "-",
            "parent": {
                "parent_id": self.parent_id,
                "parent_name": self.parent.get_full_name()
            } if self.parent else "-",
            "children": sorted([
                {
                    "child_id": child.id,
                    "child_name": child.get_full_name()
                } for child in self.children
            ], key=lambda x: x["child_name"]) if self.children else "-",
            "billing_celkem": pretty_penize(kalkulace["celkem"], self.billing_currency),
            "billing_hlavni_trida": pretty_penize(kalkulace["prvni_trida"], self.billing_currency),
            "billing_vedlejsi_trida": pretty_penize(kalkulace["vedlejsi_trida"], self.billing_currency),
            "billing_ubytovani": pretty_penize(kalkulace["ubytovani"], self.billing_currency),
            "billing_snidane": pretty_penize(kalkulace["snidane"], self.billing_currency),
            "billing_obedy": pretty_penize(kalkulace["obedy"], self.billing_currency),
            "billing_vecere": pretty_penize(kalkulace["vecere"], self.billing_currency),
            "billing_dar": pretty_penize(kalkulace["dar"], self.billing_currency),
            "strava_snidane": "info o snidanich",
            "strava_obedy": "info o obedech",
            "strava_vecere": "info o vecerich",
            "meals_top_visible": "Tady bude shrnutí info o jídle nahoru",
            "hlavni_trida_1": {
                "name": self.main_class_priority_1.full_name_cz if self.main_class_priority_1 else "-",
                "link": "/organizator/detail_tridy/" + str(self.main_class_id_priority_1) if self.main_class_priority_1 else None
            },
            "hlavni_trida_2": {
                "name": self.main_class_priority_2.full_name_cz if self.main_class_priority_2 else "-",
                "link": "/organizator/detail_tridy/" + str(self.main_class_id_priority_2) if self.main_class_priority_2 else None
            },
            "vedlejsi_trida": {
                "name": self.secondary_class.full_name_cz if self.secondary_class else "-",
                "link": "/organizator/detail_tridy/" + str(self.secondary_class_id) if self.secondary_class else None
            }
        }
    
    
    
    
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
            "billing_date_paid": self.billing_date_paid.strftime("%Y-%m-%d") if self.billing_date_paid else None,
            "billing_correction": self.billing_correction,
            "billing_correction_reason": self.billing_correction_reason,
            "billing_food_correction": self.billing_food_correction,
            "billing_food_correction_reason": self.billing_food_correction_reason,
            "billing_accomodation_correction": self.billing_accomodation_correction,
            "billing_accomodation_correction_reason": self.billing_accomodation_correction_reason,
            "billing_gift": self.billing_gift,
            
            "is_tutor": True if Role.get_by_system_name("tutor") in self.roles else False,
            "tutor_travel": self.tutor_travel,
            "tutor_license_plate": self.tutor_license_plate,
            "tutor_arrival": self.tutor_arrival,
            "tutor_departure": self.tutor_departure,
            "tutor_accompanying_names": self.tutor_accompanying_names,
            "tutor_address": self.tutor_address,
            "tutor_date_of_birth": self.tutor_date_of_birth.strftime("%Y-%m-%d") if self.tutor_date_of_birth else None,
            "tutor_bank_account": self.tutor_bank_account,
            
            "must_change_password_upon_login": "Ano" if self.must_change_password_upon_login else "Ne",
            "confirmed_email": "Ano" if self.confirmed_email else "Ne",
            "is_locked": "Ano" if self.is_locked else "Ne",
            "parent": {
                "parent_id": self.parent_id,
                "parent_name": self.parent.get_full_name()
            } if self.parent else None,
            
            "main_class_id_priority_1": self.main_class_priority_1.id if self.main_class_priority_1 else None,
            "main_class_id_priority_2": self.main_class_priority_2.id if self.main_class_priority_2 else None,
            "secondary_class_id": self.secondary_class.id if self.secondary_class else None,
            #TODO tady určitě přibudou meals a children
        }
    
    def nacist_zmeny_z_requestu(self, request):
        
        if request.form.get("main_class_id_priority_1") != self.main_class_id_priority_1:
            self.datetime_class_pick = datetime.now(tz=timezone.utc)
        if request.form.get("main_class_id_priority_1") == "-":
            self.datetime_class_pick = None
            
        self.name = request.form.get("name")
        self.surname = request.form.get("surname")
        self.email = request.form.get("email")
        self.phone = request.form.get("phone")
        self.is_student = True if request.form.get("is_student") == "Ano" else False
        self.is_ssh_member = True if request.form.get("is_ssh_member") == "Ano" else False
        self.is_active_participant = True if request.form.get("is_active_participant") == "active" else False
        self.is_student_of_partner_zus = True if request.form.get("is_student_of_partner_zus") == "Ano" else False
        self.accomodation_type = request.form.get("accomodation_type")
        self.accomodation_count = int(request.form.get("accomodation_count")) if request.form.get("accomodation_count") else 0
        self.musical_education = request.form.get("musical_education")
        self.musical_instrument = request.form.get("musical_instrument")
        self.repertoire = request.form.get("repertoire")
        self.comment = request.form.get("comment")
        self.admin_comment = request.form.get("admin_comment")
        self.billing_currency = request.form.get("billing_currency")
        self.billing_email = request.form.get("billing_email")
        self.billing_age = request.form.get("billing_age")
        self.billing_gift = int(request.form.get("billing_gift")) if request.form.get("billing_gift") else 0
        self.billing_date_paid = datetime.strptime(request.form.get("billing_date_paid"), "%Y-%m-%d") if request.form.get("billing_date_paid") else None
        self.billing_correction = int(request.form.get("billing_correction")) if request.form.get("billing_correction") else 0
        self.billing_correction_reason = request.form.get("billing_correction_reason")
        self.billing_food_correction = int(request.form.get("billing_food_correction")) if request.form.get("billing_food_correction") else 0
        self.billing_food_correction_reason = request.form.get("billing_food_correction_reason")
        self.billing_accomodation_correction = int(request.form.get("billing_accomodation_correction")) if request.form.get("billing_accomodation_correction") else 0
        self.billing_accomodation_correction_reason = request.form.get("billing_accomodation_correction_reason")
        self.main_class_id_priority_1 = int(request.form.get("main_class_id_priority_1")) if request.form.get("main_class_id_priority_1") != "-"  else None
        self.main_class_id_priority_2 = int(request.form.get("main_class_id_priority_2")) if request.form.get("main_class_id_priority_2") != "-"  else None
        self.secondary_class_id = int(request.form.get("secondary_class_id")) if request.form.get("secondary_class_id") != "-" else None
        
        self.tutor_travel = request.form.get("tutor_travel")
        self.tutor_license_plate = request.form.get("tutor_license_plate")
        self.tutor_arrival = request.form.get("tutor_arrival")
        self.tutor_departure = request.form.get("tutor_departure")
        self.tutor_accompanying_names = request.form.get("tutor_accompanying_names")
        self.tutor_address = request.form.get("tutor_address")
        self.tutor_date_of_birth = datetime.strptime(request.form.get("tutor_date_of_birth"), "%Y-%m-%d") if request.form.get("tutor_date_of_birth") else None
        self.tutor_bank_account = request.form.get("tutor_bank_account")
        
        self.must_change_password_upon_login = True if request.form.get("must_change_password_upon_login") == "Ano" else False
        self.confirmed_email = True if request.form.get("confirmed_email") == "Ano" else False
        self.is_locked = True if request.form.get("is_locked") == "Ano" else False
        if request.form.get("new_password"):
            self.password = generate_password_hash(request.form.get("new_password"), method="scrypt")
            self.must_change_password_upon_login = True
            
        self.update()
        
        
    def info_pro_user_detail(self) -> dict:
        kalkulace = self.kalkulace()
        billing_age = "dospělý"
        if self.billing_age == "child":
            billing_age = "dítě"
        elif self.billing_age == "youth":
            billing_age = "mládež do 15 let"
            
        billing_email = self.billing_email if self.billing_email else "bude použit hlavní e-mail"
        if self.parent:
            billing_email = "bude použit e-mail nadřazeného účtu"
            
        return {
            "name": self.name if self.name else "-",
            "surname": self.surname if self.surname else "-",
            "email": self.email,
            "phone": self.phone if self.phone else "-",
            "is_student": "Ano" if self.is_student else "Ne",
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "aktivní" if self.is_active_participant else "pasivní",
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else "-",
            "accomodation_type": self.accomodation_type,
            "musical_education": self.musical_education if self.musical_education else "-",
            "musical_instrument": self.musical_instrument if self.musical_instrument else "-",
            "repertoire": self.repertoire if self.repertoire else "-",
            "comment": self.comment if self.comment else "-",
            "main_class_priority_1": self.main_class_priority_1.full_name_cz if self.main_class_priority_1 else "-",
            "main_class_priority_2": self.main_class_priority_2.full_name_cz if self.main_class_priority_2 else "-",
            "secondary_class": self.secondary_class.full_name_cz if self.secondary_class else "-",
            "billing_email": billing_email,
            "billing_age": billing_age,
            "billing_date_paid": pretty_datetime(self.billing_date_paid) if self.billing_date_paid else "-",
            "billing_celkem": pretty_penize(kalkulace["celkem"], self.billing_currency),
            "billing_hlavni_trida": pretty_penize(kalkulace["prvni_trida"], self.billing_currency),
            "billing_vedlejsi_trida": pretty_penize(kalkulace["vedlejsi_trida"], self.billing_currency),
            "billing_ubytovani": pretty_penize(kalkulace["ubytovani"], self.billing_currency),
            "billing_snidane": pretty_penize(kalkulace["snidane"], self.billing_currency),
            "billing_obedy": pretty_penize(kalkulace["obedy"], self.billing_currency),
            "billing_vecere": pretty_penize(kalkulace["vecere"], self.billing_currency),
            "billing_dar": pretty_penize(kalkulace["dar"], self.billing_currency),
            "billing_correction": pretty_penize(self.billing_correction, self.billing_currency),
            "billing_correction_reason": self.billing_correction_reason,
            "billing_food_correction": pretty_penize(self.billing_food_correction, self.billing_currency),
            "billing_food_correction_reason": self.billing_food_correction_reason,
            "billing_accomodation_correction": pretty_penize(self.billing_accomodation_correction, self.billing_currency),
            "billing_accomodation_correction_reason": self.billing_accomodation_correction_reason,
            "tutor_travel": self.tutor_travel,
            "tutor_license_plate": self.tutor_license_plate,
            "tutor_arrival": self.tutor_arrival,
            "tutor_departure": self.tutor_departure,
            "tutor_accompanying_names": self.tutor_accompanying_names,
            "tutor_address": self.tutor_address,
            "tutor_date_of_birth": pretty_datetime(self.tutor_date_of_birth) if self.tutor_date_of_birth else "-",
            "tutor_bank_account": self.tutor_bank_account,
            "must_change_password_upon_login": "Ano" if self.must_change_password_upon_login else "Ne",
            "confirmed_email": "Ano" if self.confirmed_email else "Ne",
            "is_locked": "Ano" if self.is_locked else "Ne",
            "datetime_created": pretty_datetime(self.datetime_created),
            "parent": self.parent.get_full_name() if self.parent else "-",
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name()
                } for child in self.children
            ]
        }
        
# TODO procistit importy a dat je nahoru
from datetime import date
from io import BytesIO
from openpyxl import Workbook
import czech_sort
    
    
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