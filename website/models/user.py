from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from website.models.trida import Trida, user_secondary_class_jointable
from website.models.billing import Billing
from website.models.role import Role
from website.models.meal_order import Meal_order
from website.models.meal import Meal
from website.helpers.pretty_date import pretty_datetime
from website.helpers.pretty_penize import pretty_penize
from website.helpers.settings_manager import get_settings
from datetime import datetime, timedelta, timezone
from flask import current_app, flash
from flask_login import UserMixin, login_user, current_user
import jwt
from werkzeug.security import generate_password_hash
import sqlalchemy


class User(Common_methods_db_model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # personal data
    name = db.Column(db.String(200))
    surname = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    is_student = db.Column(db.Boolean, default=False)
    is_under_16 = db.Column(db.Boolean, default=False)
    
    #automatic data
    datetime_created = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    
    #valtice data
    is_ssh_member = db.Column(db.Boolean, default=False)
    is_active_participant = db.Column(db.Boolean, default=True)
    is_student_of_partner_zus = db.Column(db.Boolean, default=False)
    datetime_class_pick = db.Column(db.DateTime) # udrzuje datum picknuti hlavni tridy
    datetime_registered = db.Column(db.DateTime)
    datetime_calculation_email = db.Column(db.DateTime) # TODO je to v db modelu ale jeste to neni nikam propojeny
    accomodation_type = db.Column(db.String(200), default=None) # own/vs/gym. None znamená, že ještě nepicknul
    accomodation_count = db.Column(db.Integer, default=0)
    musical_education = db.Column(db.Text)
    musical_instrument = db.Column(db.String(1000))
    repertoire = db.Column(db.Text)
    comment = db.Column(db.Text)
    admin_comment = db.Column(db.Text)
    meals = db.Column(db.Boolean, default=False)
    
    #billing data
    billing_currency = db.Column(db.String(200), default="czk" ) # czk/eur
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
    primary_class_id = db.Column(db.Integer, db.ForeignKey("trida.id"))
    primary_class = db.relationship("Trida", back_populates="primary_participants", foreign_keys=[primary_class_id])
    secondary_classes = db.relationship("Trida",secondary=user_secondary_class_jointable, back_populates="secondary_participants")

    
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
            "email": self.email if self.email else self.parent.email,
            "registrovan": "Registrován" if self.datetime_registered else "-",
            "hlavni_trida": self.primary_class.short_name_cz if self.primary_class else "-",
            "hlavni_trida_id": self.primary_class_id
        }
    
    def info_pro_seznam_lektoru(self) -> dict:
        full_name = self.get_full_name()
        return {
            "id": self.id,
            "full_name": full_name if full_name else "-",
            "surname": self.surname if self.surname else "-",
            "phone": self.phone if self.phone else "-",
            "email": self.email,
            "taught_classes":[
                {
                    "id": trida.id,
                    "short_name": trida.short_name_cz
                } for trida in sorted(self.taught_classes, key=lambda x: czech_sort.key(x.short_name_cz))
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
        return sorted(result, key=lambda x: czech_sort.key(x["surname"] if x["surname"] else ""))
    
    
    def login(self):
        login_user(self, remember=True)
        self.update()
        
        
    def get_info_pro_seznam_useru(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
        }
        
    
    def _save_meals(self, request):
        if request.form.get("wants_meal") == "ne":
            for mo in self.meal_orders:
                mo.delete()
            return
        if request.form.get("meals"):
            for mo in self.meal_orders:
                mo.delete()
            for meal_id, count in zip(request.form.getlist("meals"), request.form.getlist("counts")):
                if meal_id == "-":
                    continue
                try:
                    mo = Meal_order(user_id=self.id, meal_id=meal_id, count=count)
                    mo.update()
                except sqlalchemy.exc.IntegrityError:
                    db.session.rollback() # protože tam vadí ten mo pending error
                    meal = Meal.get_by_id(meal_id)
                    flash(f"Chyba: jídlo {meal.get_description_cz()} bylo zapsáno více než jednou.", "error")
                    continue
    
    
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
                if self.is_under_16:
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

        
        hlavni_trida = calculate_trida(self.primary_class, self, False)
        vedlejsi_tridy = []
        for trida in self.secondary_classes:
            vedlejsi_tridy.append(calculate_trida(trida, self, True))
        
        pasivni_ucast = None
        if not self.is_active_participant:
            if self.billing_currency == "czk":
                pasivni_ucast = Billing.get_by_system_name("kurzovne_pasivni").czk
            else:
                pasivni_ucast = Billing.get_by_system_name("kurzovne_pasivni").eur
                
        
        
        
        # strava - chatgpt tohle dokaze napsat pomoci dictionaries, to se pouzije kdybych nekdy potreboval pridat neco jako typ
        if not self.meals:
            snidane = None
            obedy = None
            vecere = None
        else:
            snidane = 0
            obedy = 0
            vecere = 0
            for meal_order in self.meal_orders:
                meal = meal_order.meal
                
                if meal.type == "breakfast":
                    if meal.location == "zs":
                        if self.billing_currency == "czk":
                            snidane += meal_order.count * Billing.get_by_system_name("snidane_zs").czk
                        elif self.billing_currency == "eur":
                            snidane += meal_order.count * Billing.get_by_system_name("snidane_zs").eur
                    elif meal.location == "vs":
                        if self.billing_currency == "czk":
                            snidane += meal_order.count * Billing.get_by_system_name("snidane_ss").czk
                        elif self.billing_currency == "eur":
                            snidane += meal_order.count * Billing.get_by_system_name("snidane_ss").eur
                elif meal.type == "lunch":
                    if meal.location == "zs":
                        if self.billing_currency == "czk":
                            obedy += meal_order.count * Billing.get_by_system_name("obed_zs").czk
                        elif self.billing_currency == "eur":
                            obedy += meal_order.count * Billing.get_by_system_name("obed_zs").eur
                    elif meal.location == "vs":
                        if self.billing_currency == "czk":
                            obedy += meal_order.count * Billing.get_by_system_name("obed_ss").czk
                        elif self.billing_currency == "eur":
                            obedy += meal_order.count * Billing.get_by_system_name("obed_ss").eur
                elif meal.type == "dinner":
                    if meal.location == "zs":
                        if self.billing_currency == "czk":
                            vecere += meal_order.count * Billing.get_by_system_name("vecere_zs").czk
                        elif self.billing_currency == "eur":
                            vecere += meal_order.count * Billing.get_by_system_name("vecere_zs").eur
                    elif meal.location == "vs":
                        if self.billing_currency == "czk":
                            vecere += meal_order.count * Billing.get_by_system_name("vecere_ss").czk
                        elif self.billing_currency == "eur":
                            vecere += meal_order.count * Billing.get_by_system_name("vecere_ss").eur

        
        pasivni_ucast_do_sumy = pasivni_ucast if pasivni_ucast is not None else 0
        hlavni_trida_do_sumy = hlavni_trida if hlavni_trida is not None else 0
        vedlejsi_tridy_do_sumy = sum(vedlejsi_tridy) if vedlejsi_tridy else 0
        ubytko_do_sumy = ubytko if ubytko is not None else 0
        snidane = snidane if snidane is not None else 0
        snidane_do_sumy = snidane if snidane is not None else 0
        obedy_do_sumy = obedy if obedy is not None else 0
        vecere_do_sumy = vecere if vecere is not None else 0
        result = {
            "ubytovani": ubytko,
            "pasivni_ucast": pasivni_ucast,
            "hlavni_trida": hlavni_trida,
            "vedlejsi_tridy": vedlejsi_tridy,
            "snidane": snidane,
            "obedy": obedy,
            "vecere": vecere,
            "dar": self.billing_gift,
            "celkem": ubytko_do_sumy + snidane_do_sumy + obedy_do_sumy + vecere_do_sumy + self.billing_gift + pasivni_ucast_do_sumy + hlavni_trida_do_sumy + vedlejsi_tridy_do_sumy + self.billing_correction + self.billing_food_correction + self.billing_accomodation_correction
        }
        return result
    
    
    def info_pro_detail(self):
        # ubytovani
        if self.accomodation_type == "own":
            ubytovani = "vlastní"
        elif self.accomodation_type is None:
            ubytovani = "Zatím nevybráno"
        elif self.accomodation_type == "vs":
            ubytovani = f"vinařská škola: {self.accomodation_count}"
        else:
            ubytovani = f"tělocvična: {self.accomodation_count}"
                
        kalkulace = self.kalkulace()
        
        billing_vedlejsi_tridy_list = []
        for trida, calc in zip(self.secondary_classes, kalkulace["vedlejsi_tridy"]):
            zaznam = trida.full_name_cz + ": " + pretty_penize(calc, self.billing_currency)
            billing_vedlejsi_tridy_list.append(zaznam)
        billing_vedlejsi_tridy = "\n".join(billing_vedlejsi_tridy_list)
        
        return {
            "name": self.name if self.name else "-",
            "surname": self.surname if self.surname else "-",
            "full_name": self.get_full_name(),
            "email": self.email,
            "phone": self.phone if self.phone else "-",
            "is_student": "Ano" if self.is_student else "Ne",
            "age_category": "Do 15 let včetně" if self.is_under_16 else "16 a více let",
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
            "wants_meals": self.meals,
            "meals": [
                {
                    "popis": meal_order.meal.get_description_cz(),
                    "count": meal_order.count
                } for meal_order in sorted(self.meal_orders)
            ],
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
                } for trida in sorted(self.taught_classes, key=lambda x: czech_sort.key(x.short_name_cz))
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
            ], key=lambda x: czech_sort.key(x["child_name"])) if self.children else "-",
            "billing_celkem": pretty_penize(kalkulace["celkem"], self.billing_currency),
            "billing_pasivni_ucast": pretty_penize(kalkulace["pasivni_ucast"], self.billing_currency),
            "billing_hlavni_trida": pretty_penize(kalkulace["hlavni_trida"], self.billing_currency),
            "billing_vedlejsi_tridy": billing_vedlejsi_tridy,
            "billing_ubytovani": pretty_penize(kalkulace["ubytovani"], self.billing_currency),
            "billing_snidane": pretty_penize(kalkulace["snidane"], self.billing_currency),
            "billing_obedy": pretty_penize(kalkulace["obedy"], self.billing_currency),
            "billing_vecere": pretty_penize(kalkulace["vecere"], self.billing_currency),
            "billing_dar": pretty_penize(kalkulace["dar"], self.billing_currency),
            "meals_top_visible": "Tady bude shrnutí info o jídle nahoru",
            "hlavni_trida": {
                "name": self.primary_class.full_name_cz if self.primary_class else "-",
                "link": "/organizator/detail_tridy/" + str(self.primary_class_id) if self.primary_class else None
            },
            "vedlejsi_tridy":[
                {
                    "name": trida.full_name_cz,
                    "link": "/organizator/detail_tridy/" + str(trida.id)
                } for trida in sorted(self.secondary_classes, key=lambda x: czech_sort.key(x.full_name_cz))
            ]
        }
    
    
    def info_pro_upravu(self):
        return {
            "name": self.name if self.name else "",
            "surname": self.surname if self.surname else "",
            "email": self.email,
            "phone": self.phone,
            "is_student": "Ano" if self.is_student else "Ne",
            "age_category": "child" if self.is_under_16 else "adult",
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
            "wants_meal": "ano" if self.meals else "ne",
            "meals": [
                {
                    "meal_id": meal_order.meal_id,
                    "count": meal_order.count
                } for meal_order in sorted(self.meal_orders)
            ],
            "billing_currency": self.billing_currency,
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
            
            "primary_class_id": self.primary_class_id if self.primary_class_id else None,
            "secondary_classes": [trida.id for trida in self.secondary_classes],
        }
    
    def nacist_zmeny_z_org_requestu(self, request):
        
        if request.form.get("primary_class_id") != self.primary_class_id:
            self.datetime_class_pick = datetime.now(tz=timezone.utc)
        if request.form.get("primary_class_id") == "-":
            self.datetime_class_pick = None
            
        if request.form.get("is_active_participant") == "passive":
            self.primary_class = None
            self.secondary_classes = []
        else:
            self.primary_class_id = int(request.form.get("primary_class_id")) if request.form.get("primary_class_id") != "-"  else None
            self.secondary_classes = [int(sc) for sc in request.form.getlist("secondary_classes")]
            
             
        self.name = request.form.get("name")
        self.surname = request.form.get("surname")
        self.email = request.form.get("email")
        self.phone = request.form.get("phone")
        self.is_student = True if request.form.get("is_student") == "Ano" else False
        self.is_under_16 = True if request.form.get("age_category") == "child" else False
        self.is_ssh_member = True if request.form.get("is_ssh_member") == "Ano" else False
        self.is_active_participant = True if request.form.get("is_active_participant") == "active" else False
        self.is_student_of_partner_zus = True if request.form.get("is_student_of_partner_zus") == "Ano" else False
        self.accomodation_type = request.form.get("accomodation_type") if request.form.get("accomodation_type") != "-" else None
        self.accomodation_count = int(request.form.get("accomodation_count")) if request.form.get("accomodation_count") else 0
        self.musical_education = request.form.get("musical_education")
        self.musical_instrument = request.form.get("musical_instrument")
        self.repertoire = request.form.get("repertoire")
        self.comment = request.form.get("comment")
        self.admin_comment = request.form.get("admin_comment")
        self.meals = True if request.form.get("wants_meal") == "ano" else False
        self._save_meals(request)
        
        self.billing_currency = request.form.get("billing_currency")
        self.billing_gift = int(request.form.get("billing_gift")) if request.form.get("billing_gift") else 0
        self.billing_date_paid = datetime.strptime(request.form.get("billing_date_paid"), "%Y-%m-%d") if request.form.get("billing_date_paid") else None
        self.billing_correction = int(request.form.get("billing_correction")) if request.form.get("billing_correction") else 0
        self.billing_correction_reason = request.form.get("billing_correction_reason")
        self.billing_food_correction = int(request.form.get("billing_food_correction")) if request.form.get("billing_food_correction") else 0
        self.billing_food_correction_reason = request.form.get("billing_food_correction_reason")
        self.billing_accomodation_correction = int(request.form.get("billing_accomodation_correction")) if request.form.get("billing_accomodation_correction") else 0
        self.billing_accomodation_correction_reason = request.form.get("billing_accomodation_correction_reason")
        
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
            
        
        #ubytovani
        settings = get_settings()
        if not self.accomodation_type:
            accomodation_message = "Ubytování zatím není vybráno."
        elif self.accomodation_type == "own":
            accomodation_message = "Ubytování máte vlastní."
        else:
            if self.primary_class is None:
                if self.accomodation_type == "gym":
                    
                    accomodation_message = f"Máte zájem o ubytování v tělocvičně, počet míst: {self.accomodation_count}. Do fronty ale budete zařazeni až po přihlášení do třídy."
                elif self.accomodation_type == "vs":
                    accomodation_message = f"Máte zájem o ubytování na vinařské škole, počet míst: {self.accomodation_count}. Do fronty ale budete zařazeni až po přihlášení do třídy."
            else:
                users = sorted(filter(lambda x: x.primary_class_id, User.get_all()), key=lambda x: x.datetime_class_pick)
                mist_vycerpano_gym = 0
                mist_vycerpano_vs = 0
                for user in users:
                    user: User
                    if user == current_user:
                        break
                    if user.accomodation_type == "gym" and user.primary_class:
                        mist_vycerpano_gym += user.accomodation_count
                    elif user.accomodation_type == "vs" and user.primary_class:
                        mist_vycerpano_vs += user.accomodation_count
                if self.accomodation_type == "gym":
                    poradi_list = []
                    for i in range(user.accomodation_count):
                        poradi_list.append(f"{mist_vycerpano_gym+i+1}/{settings['gym_capacity']}")
                    poradi_display = ", ".join(poradi_list)
                    accomodation_message = f"Máte zájem o ubytování v tělocvičně. Pořadí Vašich míst ve frontě je: {poradi_display}."
                if self.accomodation_type == "vs":
                    poradi_list = []
                    for i in range(user.accomodation_count):
                        poradi_list.append(f"{mist_vycerpano_vs+i+1}/{settings['vs_capacity']}")
                    poradi_display = ", ".join(poradi_list)
                    accomodation_message = f"Máte zájem o ubytování na vinařské škole. Pořadí Vašich míst ve frontě je: {poradi_display}."


        return {
            "name": self.name if self.name else "-",
            "surname": self.surname if self.surname else "-",
            "email": self.email,
            "phone": self.phone if self.phone else "-",
            "is_student": "Ano" if self.is_student else "Ne",
            "age_category": "Do 15 let včetně" if self.is_under_16 else "16 a více let",
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "aktivní" if self.is_active_participant else "pasivní",
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else "-",
            "accomodation_message": accomodation_message,
            "musical_education": self.musical_education if self.musical_education else "-",
            "musical_instrument": self.musical_instrument if self.musical_instrument else "-",
            "repertoire": self.repertoire if self.repertoire else "-",
            "comment": self.comment if self.comment else "-",
            "wants_meals": True if self.meals else False,
            "meals": [
                {
                    "popis": meal_order.meal.get_description_cz(),
                    "count": meal_order.count
                } for meal_order in sorted(self.meal_orders)
            ],
            "primary_class": self.primary_class.full_name_cz if self.primary_class else "-",
            "secondary_classes": "\n".join([trida.full_name_cz for trida in sorted(self.secondary_classes, key=lambda x: czech_sort.key(x.full_name_cz))]) if self.secondary_classes else "-",
            "billing_date_paid": pretty_datetime(self.billing_date_paid) if self.billing_date_paid else "-",
            "billing_celkem": pretty_penize(kalkulace["celkem"], self.billing_currency),
            "billing_pasivni_ucast": pretty_penize(kalkulace["pasivni_ucast"], self.billing_currency),
            "billing_hlavni_trida": pretty_penize(kalkulace["hlavni_trida"], self.billing_currency),
            "billing_vedlejsi_tridy": "\n".join([trida.full_name_cz + ": " + pretty_penize(calc, self.billing_currency) for trida, calc in zip(self.secondary_classes, kalkulace["vedlejsi_tridy"])]) if self.secondary_classes else "-",
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
            "datetime_created": pretty_datetime(self.datetime_created),
            "parent": self.parent.get_full_name() if self.parent else "-",
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name()
                } for child in self.children
            ]
        }
        
    def info_pro_en_user_detail(self) -> dict:
        kalkulace = self.kalkulace()
        
         #ubytovani
        settings = get_settings()
        if not self.accomodation_type:
            accomodation_message = "The accomodation is not picked yet."
        elif self.accomodation_type == "own":
            accomodation_message = "You take care of accomodation yourself."
        else:
            if self.primary_class is None:
                if self.accomodation_type == "gym":
                    
                    accomodation_message = f"You are interested in accomodation in the gym, for {self.accomodation_count} people. You will be placed into the queue after you pick a class."
                elif self.accomodation_type == "vs":
                    accomodation_message = f"You are interested in accomodation in the viticulture school, for {self.accomodation_count} people. You will be placed into the queue after you pick a class."
            else:
                users = sorted(filter(lambda x: x.primary_class_id, User.get_all()), key=lambda x: x.datetime_class_pick)
                mist_vycerpano_gym = 0
                mist_vycerpano_vs = 0
                for user in users:
                    user: User
                    if user == current_user:
                        break
                    if user.accomodation_type == "gym" and user.primary_class:
                        mist_vycerpano_gym += user.accomodation_count
                    elif user.accomodation_type == "vs" and user.primary_class:
                        mist_vycerpano_vs += user.accomodation_count
                if self.accomodation_type == "gym":
                    poradi_list = []
                    for i in range(user.accomodation_count):
                        poradi_list.append(f"{mist_vycerpano_gym+i+1}/{settings['gym_capacity']}")
                    poradi_display = ", ".join(poradi_list)
                    accomodation_message = f"You are interested in accomodation in the gym. Your place in the queue is: {poradi_display}."
                if self.accomodation_type == "vs":
                    poradi_list = []
                    for i in range(user.accomodation_count):
                        poradi_list.append(f"{mist_vycerpano_vs+i+1}/{settings['vs_capacity']}")
                    poradi_display = ", ".join(poradi_list)
                    accomodation_message = f"You are interested in accomodation in the viticulture school. Your place in the queue is: {poradi_display}."

            
        return {
            "name": self.name if self.name else "-",
            "surname": self.surname if self.surname else "-",
            "email": self.email,
            "phone": self.phone if self.phone else "-",
            "is_student": "Yes" if self.is_student else "No",
            "age_category": "Up to and including 15 years" if self.is_under_16 else "16 years and older",
            "is_ssh_member": "Yes" if self.is_ssh_member else "No",
            "is_active_participant": "active" if self.is_active_participant else "passive",
            "is_student_of_partner_zus": "Yes" if self.is_student_of_partner_zus else "No",
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else "-",
            "accomodation_message": accomodation_message,
            "musical_education": self.musical_education if self.musical_education else "-",
            "musical_instrument": self.musical_instrument if self.musical_instrument else "-",
            "repertoire": self.repertoire if self.repertoire else "-",
            "comment": self.comment if self.comment else "-",
            "wants_meals": "ano" if self.meals else "ne",
            "meals": [
                {
                    "popis": meal_order.meal.get_description_en(),
                    "count": meal_order.count
                } for meal_order in sorted(self.meal_orders)
            ],
            "primary_class": self.primary_class.full_name_en if self.primary_class else "-",
            "secondary_classes": "\n".join([trida.full_name_en for trida in sorted(self.secondary_classes, key=lambda x: czech_sort.key(x.full_name_en))]) if self.secondary_classes else "-",
            "billing_date_paid": pretty_datetime(self.billing_date_paid) if self.billing_date_paid else "-",
            "billing_celkem": pretty_penize(kalkulace["celkem"], self.billing_currency),
            "billing_pasivni_ucast": pretty_penize(kalkulace["pasivni_ucast"], self.billing_currency),
            "billing_hlavni_trida": pretty_penize(kalkulace["hlavni_trida"], self.billing_currency),
            "billing_vedlejsi_tridy": "\n".join([trida.full_name_en + ": " + pretty_penize(calc, self.billing_currency) for trida, calc in zip(self.secondary_classes, kalkulace["vedlejsi_tridy"])]) if self.secondary_classes else "-",
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
            "tutor_travel": "own" if self.tutor_travel == "own" else "public",
            "tutor_license_plate": self.tutor_license_plate if self.tutor_license_plate else "-",
            "tutor_arrival": self.tutor_arrival if self.tutor_arrival else "-",
            "tutor_departure": self.tutor_departure if self.tutor_departure else "-",
            "tutor_accompanying_names": self.tutor_accompanying_names if self.tutor_accompanying_names else "-",
            "tutor_address": self.tutor_address if self.tutor_address else "-",
            "tutor_date_of_birth": pretty_datetime(self.tutor_date_of_birth) if self.tutor_date_of_birth else "-",
            "tutor_bank_account": self.tutor_bank_account if self.tutor_bank_account else "-",
            "must_change_password_upon_login": "Yes" if self.must_change_password_upon_login else "No",
            "confirmed_email": "Yes" if self.confirmed_email else "No",
            "is_locked": "Yes" if self.is_locked else "No",
            "datetime_created": pretty_datetime(self.datetime_created),
            "parent": self.parent.get_full_name() if self.parent else "-",
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name()
                } for child in self.children
            ]
        }
        
        
    def info_pro_user_upravu(self) -> dict:
        zmena_ucasti = "povolena"
        if any([self.primary_class, self.secondary_classes]):
            zmena_ucasti = "zakázána"
        return {
            "name": self.name if self.name else "",
            "surname": self.surname if self.surname else "",
            "email": self.email,
            "phone": self.phone,
            "is_student": "Ano" if self.is_student else "Ne",
            "age_category": "child" if self.is_under_16 else "adult",
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "active" if self.is_active_participant else "passive",
            "zmena_ucasti": zmena_ucasti,
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "accomodation_type": self.accomodation_type,
            "accomodation_count": self.accomodation_count,
            "musical_education": self.musical_education,
            "musical_instrument": self.musical_instrument,
            "repertoire": self.repertoire,
            "comment": self.comment,
            "wants_meal": "ano" if self.meals else "ne",
            "meals": [
                {
                    "meal_id": meal_order.meal_id,
                    "count": meal_order.count
                } for meal_order in sorted(self.meal_orders)
            ],
            "billing_currency": self.billing_currency,
            "billing_gift": self.billing_gift,
            "has_parent": True if self.parent else False,
            "manager_name": self.parent.get_full_name() if self.parent else "",
            "tutor_travel": self.tutor_travel,
            "tutor_license_plate": self.tutor_license_plate,
            "tutor_arrival": self.tutor_arrival,
            "tutor_departure": self.tutor_departure,
            "tutor_accompanying_names": self.tutor_accompanying_names,
            "tutor_address": self.tutor_address,
            "tutor_date_of_birth": self.tutor_date_of_birth.strftime("%Y-%m-%d") if self.tutor_date_of_birth else None,
            "tutor_bank_account": self.tutor_bank_account,
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name()
                } for child in self.children
            ],
        }   
        
        
    def info_pro_en_user_upravu(self) -> dict: # stejny jako cz verze, ale z duvodu konsistence to tu nechavam zalozene
        zmena_ucasti = "povolena"
        if any([self.primary_class, self.secondary_classes]):
            zmena_ucasti = "zakázána"
        return {
            "name": self.name if self.name else "",
            "surname": self.surname if self.surname else "",
            "email": self.email,
            "phone": self.phone,
            "is_student": "Ano" if self.is_student else "Ne",
            "age_category": "child" if self.is_under_16 else "adult",
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "active" if self.is_active_participant else "passive",
            "zmena_ucasti": zmena_ucasti,
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "accomodation_type": self.accomodation_type,
            "accomodation_count": self.accomodation_count,
            "musical_education": self.musical_education,
            "musical_instrument": self.musical_instrument,
            "repertoire": self.repertoire,
            "comment": self.comment,
            "wants_meal": "ano" if self.meals else "ne",
            "meals": [
                {
                    "meal_id": meal_order.meal_id,
                    "count": meal_order.count
                } for meal_order in sorted(self.meal_orders)
            ],
            "billing_currency": self.billing_currency,
            "billing_gift": self.billing_gift,
            "has_parent": True if self.parent else False,
            "manager_name": self.parent.get_full_name() if self.parent else "",
            "tutor_travel": self.tutor_travel,
            "tutor_license_plate": self.tutor_license_plate,
            "tutor_arrival": self.tutor_arrival,
            "tutor_departure": self.tutor_departure,
            "tutor_accompanying_names": self.tutor_accompanying_names,
            "tutor_address": self.tutor_address,
            "tutor_date_of_birth": self.tutor_date_of_birth.strftime("%Y-%m-%d") if self.tutor_date_of_birth else None,
            "tutor_bank_account": self.tutor_bank_account,
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name()
                } for child in self.children
            ],
        }  
    
    
    def nacist_zmeny_z_user_requestu(self, request):
        self.name = request.form.get("name")
        self.surname = request.form.get("surname")
        self.phone = request.form.get("phone")
        self.is_student = True if request.form.get("is_student") == "Ano" else False
        self.is_under_16 = True if request.form.get("age_category") == "child" else False
        self.is_ssh_member = True if request.form.get("is_ssh_member") == "Ano" else False
        self.is_active_participant = True if request.form.get("is_active_participant") == "active" else False
        self.is_student_of_partner_zus = True if request.form.get("is_student_of_partner_zus") == "Ano" else False
        self.accomodation_type = request.form.get("accomodation_type") if request.form.get("accomodation_type") != "-" else None
        self.accomodation_count = int(request.form.get("accomodation_count")) if request.form.get("accomodation_count") else 0
        self.musical_education = request.form.get("musical_education")
        self.musical_instrument = request.form.get("musical_instrument")
        self.repertoire = request.form.get("repertoire")
        self.comment = request.form.get("comment")
        
        self.meals = True if request.form.get("wants_meal") == "ano" else False
        self._save_meals(request)
        
        self.billing_currency = request.form.get("billing_currency")
        self.billing_gift = int(request.form.get("billing_gift")) if request.form.get("billing_gift") else 0
        
        self.tutor_travel = request.form.get("tutor_travel")
        self.tutor_license_plate = request.form.get("tutor_license_plate")
        self.tutor_arrival = request.form.get("tutor_arrival")
        self.tutor_departure = request.form.get("tutor_departure")
        self.tutor_accompanying_names = request.form.get("tutor_accompanying_names")
        self.tutor_address = request.form.get("tutor_address")
        self.tutor_date_of_birth = datetime.strptime(request.form.get("tutor_date_of_birth"), "%Y-%m-%d") if request.form.get("tutor_date_of_birth") else None
        self.tutor_bank_account = request.form.get("tutor_bank_account")
        
        if request.form.get("new_password"):
            self.password = generate_password_hash(request.form.get("new_password"), method="scrypt")
        # parent_email je vyresenej ve view
        # zmena emailu je taky ve view
        
        self.update()
        

    def info_for_tutor(self) -> dict:
        return {
            "full_name": self.get_full_name(),
            "email": self.email,
            "phone": self.phone,
            "education": self.musical_education,
            "repertoire": self.repertoire,
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
    #                 entry["Kurzovné"] = u.kalkulace()["hlavni_trida"] + u.kalkulace()["vedlejsi_trida"]
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