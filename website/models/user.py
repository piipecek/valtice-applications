import sqlalchemy
import sqlalchemy.exc
from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from website.models.trida import Trida, user_secondary_class_jointable
from website.models.billing import Billing
from website.models.role import Role
from website.models.meal_order import Meal_order
from website.models.meal import Meal
from website.helpers.pretty_date import pretty_datetime, pretty_date
from website.helpers.pretty_penize import pretty_penize
from website.helpers.settings_manager import get_settings
from website.mail_handler import mail_sender
from datetime import datetime, timedelta, timezone, date
from flask import current_app, flash, url_for
from flask_login import UserMixin, login_user
from io import BytesIO
from openpyxl import Workbook
import jwt
import czech_sort
import sqlalchemy
from werkzeug.security import generate_password_hash


class User(Common_methods_db_model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # personal data
    name = db.Column(db.String(200))
    surname = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    is_student = db.Column(db.Boolean, default=False)
    is_under_16 = db.Column(db.Boolean, default=False)
    
    #automatic data
    datetime_created = db.Column(db.DateTime, default=datetime.now)
    
    #valtice data
    is_this_year_participant = db.Column(db.Boolean, default=True) # pri registraci se je to nebude ptat na letosek zejo, to ma efekt az za rok
    is_ssh_member = db.Column(db.Boolean, default=False)
    is_active_participant = db.Column(db.Boolean, default=True)
    is_student_of_partner_zus = db.Column(db.Boolean, default=False)
    datetime_class_pick = db.Column(db.DateTime) # udrzuje datum picknuti hlavni tridy
    datetime_registered = db.Column(db.DateTime)
    datetime_calculation_email = db.Column(db.DateTime)
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
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec) # tady je utc spravne, verifikace ho taky pouziva
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
    
    def get_full_name(self, lang: str = "cz") -> str:
        def is_blank(s):
            return s is None or s.strip() == ""

        has_name = not is_blank(self.name)
        has_surname = not is_blank(self.surname)

        if has_name or has_surname:
            return f"{self.name or ''} {self.surname or ''}".strip()

        if self.email:
            return self.email

        if self.parent:
            parent_name = f"{self.parent.name or ''} {self.parent.surname or ''}".strip()
            if parent_name:
                suffix = "'s child" if lang != "cz" else " - dítě"
                return f"{parent_name}{suffix}"
            if self.parent.email:
                suffix = "'s child" if lang != "cz" else " - dítě"
                return f"{self.parent.email}{suffix}"

        # tohle by nemělo nastat, cuz rodič dycky má email
        return "Zatím beze jména" if lang == "cz" else "Not yet named"
    
    
    def info_pro_seznam_ucastniku(self) -> dict:
        full_name = self.get_full_name("cz")
        return {
            "id": self.id,
            "full_name": full_name if full_name else "-",
            "surname": self.surname if self.surname else "-",
            "email": self.email if self.email else self.parent.email if self.parent else "-",
            "registrovan": "Registrován" if self.datetime_registered else "-",
            "hlavni_trida": self.primary_class.short_name_cz if self.primary_class else "-",
            "hlavni_trida_id": self.primary_class_id
        }
        
    
    def info_pro_seznam_uctu(self) -> dict:
        full_name = self.get_full_name("cz")
        return {
            "id": self.id,
            "full_name": full_name if full_name else "-",
            "email": self.email if self.email else self.parent.email if self.parent else "-",
            "datum": pretty_date(self.datetime_created)
        }
    
    
    def info_pro_seznam_lektoru(self) -> dict:
        full_name = self.get_full_name("cz")
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
                "name": u.get_full_name("cz")
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
                    "full_name": u.get_full_name("cz"),
                    "surname": u.surname
                }
                result.append(data)
        return sorted(result, key=lambda x: czech_sort.key(x["surname"] or ""))
    
    
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
                if trida.secondary_billing_behavior == "free": # napr. zapsanej sbor jako vedlejsi trida
                    return 0
                elif trida.secondary_billing_behavior == "ensemble":
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
        print(snidane, obedy, vecere)

        
        pasivni_ucast_do_sumy = pasivni_ucast if pasivni_ucast is not None else 0
        hlavni_trida_do_sumy = hlavni_trida if hlavni_trida is not None else 0
        vedlejsi_tridy_do_sumy = sum(vedlejsi_tridy) if vedlejsi_tridy else 0
        ubytko_do_sumy = ubytko if ubytko is not None else 0
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
    
    
    def _get_first_enrolled_child(self):
        # pokud jsem doprovod, zjistit, ktery z mejch deti se kliklo jako prvni
        all_children = [c for c in self.children if c.is_under_16]
        if all_children:
            children = sorted(filter(lambda y: y.primary_class_id, self.children), key=lambda x: x.datetime_class_pick)
            return children[0] if children else None       
        return None
    
    
    def _kolik_mista_zabiram(self):
        # vrati to muj accomodation_count + accomodation_count myho doprovodu, pokud jsem first enrolled child
        result = self.accomodation_count
        if self.parent:
            rozhodujici_dite = self.parent._get_first_enrolled_child()
            if rozhodujici_dite and rozhodujici_dite == self and not self.parent.is_active_participant:
                result += self.parent.accomodation_count
        return result
    
    
    def ubytovani(self) -> dict:
        # tohle je vystup
        result = {
            "accomodation_message_cz": None,
            "accomodation_message_en": None,
            "fits": False, # momentalne to neni nikde jinde vyuzivany. Puvodne to slouzilo tak, ze kalkulace nepocitala ubytko, pokud se clovek nevejde. To bylo ale nezadouci.
        }
        
        settings = get_settings()
        
        if not self.accomodation_type:
            result["accomodation_message_cz"] = "Ubytování zatím není vybráno."
            result["accomodation_message_en"] = "Accommodation not selected yet."
            return result
        elif self.accomodation_type == "own":
            result["accomodation_message_cz"] = "Ubytování máte vlastní."
            result["accomodation_message_en"] = "You have your own accommodation."
            return result
        else:
            if not self.is_active_participant:
                # moje volba mista ubytovani nema roli, je to podle meho doprovodu
                # pokud nejsem doprovod, nemam narok na ubytovani
                children = [c for c in self.children if c.is_under_16]
                if len(children) == 0:
                    result["accomodation_message_cz"] = "Nemáte nárok na ubytování, protože nejste aktivní účastník a nejste doprovod dětského účastníka."
                    result["accomodation_message_en"] = "You are not entitled to accommodation because you are not an active participant and you are not the parent of a child participant."
                    return result
                else:
                    # pokud jsem doprovod, zjistit, ktery z mejch deti se kliklo jako prvni a pripocitat se k nemu
                    # je tu trochu duplikace kodu o par radku niz, hmm
                    users = sorted(filter(lambda x: x.primary_class_id, User.get_all()), key=lambda x: x.datetime_class_pick)
                    mist_vycerpano_gym = 0
                    mist_vycerpano_vs = 0
                    rozhodujici_dite: User = self._get_first_enrolled_child()
                    if not rozhodujici_dite:
                        result["accomodation_message_cz"] = "Máte zájem o ubytování, ale do fronty budete zařazeni, teprve až se do třídy přihlásí jeden z Vašich podřízených účtů."
                        result["accomodation_message_en"] = "You are interested in accommodation, but you will be placed in the queue only after one of your child accounts signs up for the class."
                        return result
                    else:
                        for user in users:
                            user: User
                            if user == rozhodujici_dite:
                                break
                            if user.accomodation_type == "gym" and user.primary_class:
                                mist_vycerpano_gym += user._kolik_mista_zabiram()
                            elif user.accomodation_type == "vs" and user.primary_class:
                                mist_vycerpano_vs += user._kolik_mista_zabiram()
                        if rozhodujici_dite.accomodation_type == "gym":
                            poradi_list = []
                            for i in range(rozhodujici_dite.accomodation_count + self.accomodation_count):
                                if mist_vycerpano_gym+i+1 < int(settings["gym_capacity"]):
                                    result["fits"] = True
                                poradi_list.append(f"{mist_vycerpano_gym+i+1}/{settings['gym_capacity']}")
                            poradi_display = ", ".join(poradi_list)
                            result["accomodation_message_cz"] = f"Máte zájem o ubytování v tělocvičně společně s účtem, který doprovádíte. Pořadí vašich míst ve frontě je: {poradi_display}."
                            result["accomodation_message_en"] = f"You are interested in accommodation in the gym together with the account you are accompanying. The order of your places in the queue is: {poradi_display}."
                            return result
                        elif rozhodujici_dite.accomodation_type == "vs":
                            poradi_list = []
                            for i in range(rozhodujici_dite.accomodation_count + self.accomodation_count):
                                if mist_vycerpano_vs+i+1 < int(settings["vs_capacity"]):
                                    result["fits"] = True
                                poradi_list.append(f"{mist_vycerpano_vs+i+1}/{settings['vs_capacity']}")
                            poradi_display = ", ".join(poradi_list)
                            result["accomodation_message_cz"] = f"Máte zájem o ubytování na vinařské škole společně s účtem, který doprovázíte. Pořadí vašich míst ve frontě je: {poradi_display}."
                            result["accomodation_message_en"] = f"You are interested in accommodation at the wine school together with the account you are accompanying. The order of your places in the queue is: {poradi_display}."
                            return result
                        else:
                            if not rozhodujici_dite.accomodation_type:
                                result["accomodation_message_cz"] = "Vaše dítě si ještě nevybralo ubytování a vy jste s ním z důvodu pasivní účasti."
                                result["accomodation_message_en"] = "Your child has not yet chosen accommodation and you are with them due to passive participation."
                                return result
                            elif rozhodujici_dite.accomodation_type == "own":
                                result["accomodation_message_cz"] = "Ubytování máte společně s dítětem vlastní."
                                result["accomodation_message_en"] = "You and your child have your own accommodation."
                                return result
                        
            else:
                if self.primary_class is None:
                    if self.accomodation_type == "gym":
                        result["accomodation_message_cz"] = f"Máte zájem o ubytování v tělocvičně, počet míst: {self.accomodation_count}. Do fronty ale budete zařazeni až po přihlášení do třídy."
                        result["accomodation_message_en"] = f"You are interested in accommodation in the gym, number of places: {self.accomodation_count}. But you will be placed in the queue only after signing up for the class."
                        return result
                    elif self.accomodation_type == "vs":
                        result["accomodation_message_cz"] = f"Máte zájem o ubytování na vinařské škole, počet míst: {self.accomodation_count}. Do fronty ale budete zařazeni až po přihlášení do třídy."
                        result["accomodation_message_en"] = f"You are interested in accommodation at the wine school, number of places: {self.accomodation_count}. But you will be placed in the queue only after signing up for the class."
                        return result
                elif self.accomodation_count == 0:
                    if self.accomodation_type == "gym":
                        result["accomodation_message_cz"] = "Máte zájem o ubytování v tělocvičně, ale nevybrali jste počet míst. Kontaktujte prosím organizátory."
                        result["accomodation_message_en"] = "You are interested in accommodation in the gym, but you have not selected the number of places. Please contact the organizers."
                        return result
                    elif self.accomodation_type == "vs":
                        result["accomodation_message_cz"] = "Máte zájem o ubytování na vinařské škole, ale nevybrali jste počet míst. Kontaktujte prosím organizátory."
                        result["accomodation_message_en"] = "You are interested in accommodation at the wine school, but you have not selected the number of places. Please contact the organizers."
                        return result
                else:
                    users = sorted(filter(lambda x: x.primary_class_id, User.get_all()), key=lambda x: x.datetime_class_pick)
                    mist_vycerpano_gym = 0
                    mist_vycerpano_vs = 0
                    # nactu pocet zabranejch mist az do my pozice
                    for user in users:
                        user: User
                        if user == self:
                            break
                        if user.accomodation_type == "gym" and user.primary_class:
                            mist_vycerpano_gym += user._kolik_mista_zabiram() # tady ubiram schvalne za dite i za doprovod
                        elif user.accomodation_type == "vs" and user.primary_class:
                            mist_vycerpano_vs += user._kolik_mista_zabiram() 
                    if self.accomodation_type == "gym":
                        poradi_list = []
                        for i in range(user.accomodation_count): # tady iteruju schvalne jen pres sebe, pac doprovod to ma reseny vejs
                            if mist_vycerpano_gym+i+1 < int(settings["gym_capacity"]):
                                result["fits"] = True
                            poradi_list.append(f"{mist_vycerpano_gym+i+1}/{settings['gym_capacity']}")
                        poradi_display = ", ".join(poradi_list)
                        result["accomodation_message_cz"] = f"Máte zájem o ubytování v tělocvičně. Pořadí Vašich míst ve frontě je: {poradi_display}."
                        result["accomodation_message_en"] = f"You are interested in accommodation in the gym. The order of your places in the queue is: {poradi_display}."
                        return result
                    if self.accomodation_type == "vs":
                        poradi_list = []
                        for i in range(user.accomodation_count):
                            if mist_vycerpano_vs+i+1 < int(settings["vs_capacity"]):
                                result["fits"] = True
                            poradi_list.append(f"{mist_vycerpano_vs+i+1}/{settings['vs_capacity']}")
                        poradi_display = ", ".join(poradi_list)
                        result["accomodation_message_cz"] = f"Máte zájem o ubytování na vinařské škole. Pořadí Vašich míst ve frontě je: {poradi_display}."
                        result["accomodation_message_en"] = f"You are interested in accommodation at the wine school. The order of your places in the queue is: {poradi_display}."
                        return result
        return result
    
    
    @staticmethod
    def get_fronta_na_internat() -> str:
        result = [
            "Generuji seznam lidí, kteří mají aktivní účast, zájem o ubytování na internátě, zapsanou hlavní třídu a (jsou členy SSH nebo jim je pod 16)."
        ]
        users = User.get_all()
        users = filter(lambda x: x.is_active_participant and x.accomodation_type == "vs" and x.primary_class_id and (x.is_ssh_member or x.is_under_16), users)
        users = sorted(users, key=lambda x: x.datetime_class_pick)
        for user in users:
            zaznam = ""
            zaznam += user.get_full_name("cz")
            zaznam += f" | čas výběru tříy: {pretty_datetime(user.datetime_class_pick)}"
            zaznam += f" | počet míst: {user.accomodation_count}"
            result.append(zaznam)
            if user.parent and user.is_under_16:
                if user.parent in users:
                    result.append(f"Minulý dětský účastník je podřazený pod {user.parent.get_full_name('cz')}, který je také v tomto seznamu.")
                else:
                    result.append(f"Minulý dětský účastník je podřazený pod {user.parent.get_full_name('cz')}, který není v tomto seznamu. Jeho účast je {'aktivní' if user.parent.is_active_participant else 'pasivní'}, {'je členem SSH' if user.parent.is_ssh_member else 'není členem SSH'} a žádá o {user.parent.accomodation_count} míst na internátě.")
                
            
        return "<br>".join(result)

    def get_meals_top_visible(self) -> str:
        result_list = []
        for meal_order in sorted(self.meal_orders):
            entry = f"{meal_order.count}x {meal_order.meal.get_description_cz()}"
            result_list.append(entry)
        return ", ".join(result_list)
    
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
        
        last_billing_email_message = "Účastník zatím nedostal e-mail o platbě."
        if self.datetime_calculation_email:
            last_billing_email_message = f"Účastník dostal e-mail o platbě naposledy {pretty_datetime(self.datetime_calculation_email)}."
        
        return {
            "name": self.name if self.name else "-",
            "surname": self.surname if self.surname else "-",
            "full_name": self.get_full_name("cz"),
            "email": self.email,
            "phone": self.phone if self.phone else "-",
            "date_of_birth": pretty_date(self.date_of_birth) if self.date_of_birth else "-",
            "is_student": "Ano" if self.is_student else "Ne",
            "age_category": "Do 15 let včetně" if self.is_under_16 else "16 a více let",
            "datetime_class_pick": pretty_datetime(self.datetime_class_pick) if self.datetime_class_pick else "Zatím nevybráno",
            "datetime_created": pretty_datetime(self.datetime_created),
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_this_year_participant": "Ano" if self.is_this_year_participant else "Ne",
            "is_active_participant": "aktivní" if self.is_active_participant else "pasivní",
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else "Zatím neregistrován",
            "accomodation_message": self.ubytovani()["accomodation_message_cz"],
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
            "tutor_bank_account": self.tutor_bank_account if self.tutor_bank_account else "-",
            "must_change_password_upon_login": "Ano" if self.must_change_password_upon_login else "Ne",
            "confirmed_email": "Ano" if self.confirmed_email else "Ne",
            "is_locked": "Ano" if self.is_locked else "Ne",
            "roles": ", ".join([r.display_name for r in sorted(self.roles)]) if self.roles else "-",
            "parent": {
                "parent_id": self.parent_id,
                "parent_name": self.parent.get_full_name("cz")
            } if self.parent else "-",
            "children": sorted([
                {
                    "child_id": child.id,
                    "child_name": child.get_full_name("cz")
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
            "last_billing_email_message": last_billing_email_message,
            "meals_top_visible": self.get_meals_top_visible(),
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
            "date_of_birth": self.date_of_birth.strftime("%Y-%m-%d") if self.date_of_birth else None,
            "is_student": "Ano" if self.is_student else "Ne",
            "age_category": "child" if self.is_under_16 else "adult",
            "is_this_year_participant": "Ano" if self.is_this_year_participant else "Ne",
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
            "tutor_bank_account": self.tutor_bank_account,
            
            "must_change_password_upon_login": "Ano" if self.must_change_password_upon_login else "Ne",
            "confirmed_email": "Ano" if self.confirmed_email else "Ne",
            "is_locked": "Ano" if self.is_locked else "Ne",
            "parent": {
                "parent_id": self.parent_id,
                "parent_name": self.parent.get_full_name("cz")
            } if self.parent else None,
            
            "primary_class_id": self.primary_class_id if self.primary_class_id else "-",
            "secondary_classes": [trida.id for trida in sorted(self.secondary_classes, key=lambda x: czech_sort.key(x.full_name_cz))],
        }
    
    def nacist_zmeny_z_org_requestu(self, request):
        
        if request.form.get("primary_class_id") != str(self.primary_class_id):
            self.datetime_class_pick = datetime.now()
        if request.form.get("primary_class_id") == "-":
            self.datetime_class_pick = None
            
        if request.form.get("is_active_participant") == "passive":
            self.primary_class = None
            self.secondary_classes = []
        else:
            self.primary_class_id = int(request.form.get("primary_class_id")) if request.form.get("primary_class_id") != "-"  else None
            self.secondary_classes = []
            for id in request.form.getlist("secondary_classes"):
                trida = Trida.get_by_id(id)
                if trida not in self.secondary_classes:
                    self.secondary_classes.append(trida)
                    
        if self.billing_date_paid is None and request.form.get("billing_date_paid"):
            if self.parent:
                target = self.parent.email
            else:
                target = self.email
            mail_sender(mail_identifier="succesful_payment", target=target)

            
             
        self.name = request.form.get("name")
        self.surname = request.form.get("surname")
        self.email = request.form.get("email") if request.form.get("email") else None
        self.phone = request.form.get("phone")
        self.date_of_birth = datetime.strptime(request.form.get("date_of_birth"), "%Y-%m-%d") if request.form.get("date_of_birth") else None
        self.is_student = True if request.form.get("is_student") == "Ano" else False
        self.is_under_16 = True if request.form.get("age_category") == "child" else False
        self.is_this_year_participant = True if request.form.get("is_this_year_participant") == "Ano" else False
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
        ubytovani = self.ubytovani()

        return {
            "name": self.name if self.name else "-",
            "surname": self.surname if self.surname else "-",
            "email": self.email,
            "phone": self.phone if self.phone else "-",
            "date_of_birth": pretty_date(self.date_of_birth) if self.date_of_birth else "-",
            "is_student": "Ano" if self.is_student else "Ne",
            "age_category": "Do 15 let včetně" if self.is_under_16 else "16 a více let",
            "is_this_year_participant": "Ano" if self.is_this_year_participant else "Ne",
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "aktivní" if self.is_active_participant else "pasivní",
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else "-",
            "accomodation_message": ubytovani["accomodation_message_cz"],
            "musical_education": self.musical_education if self.musical_education else "-",
            "musical_instrument": self.musical_instrument if self.musical_instrument else "-",
            "repertoire": self.repertoire if self.repertoire else "-",
            "comment": self.comment if self.comment else "-",
            "wants_meals": self.meals,
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
            "tutor_bank_account": self.tutor_bank_account if self.tutor_bank_account else "-",
            "must_change_password_upon_login": "Ano" if self.must_change_password_upon_login else "Ne",
            "confirmed_email": "Ano" if self.confirmed_email else "Ne",
            "is_locked": "Ano" if self.is_locked else "Ne",
            "datetime_created": pretty_datetime(self.datetime_created),
            "parent": self.parent.get_full_name("cz") if self.parent else "-",
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name("cz")
                } for child in self.children
            ] if len(self.children) > 0 else "-",
        }
        
    def info_pro_en_user_detail(self) -> dict:
        kalkulace = self.kalkulace()
        ubytovani = self.ubytovani()
            
        return {
            "name": self.name if self.name else "-",
            "surname": self.surname if self.surname else "-",
            "email": self.email,
            "phone": self.phone if self.phone else "-",
            "date_of_birth": pretty_date(self.date_of_birth) if self.date_of_birth else "-",
            "is_student": "Yes" if self.is_student else "No",
            "age_category": "Up to and including 15 years" if self.is_under_16 else "16 years and older",
            "is_ssh_member": "Yes" if self.is_ssh_member else "No",
            "is_this_year_participant": "Yes" if self.is_this_year_participant else "No",
            "is_active_participant": "active" if self.is_active_participant else "passive",
            "is_student_of_partner_zus": "Yes" if self.is_student_of_partner_zus else "No",
            "datetime_registered": pretty_datetime(self.datetime_registered) if self.datetime_registered else "-",
            "accomodation_message": ubytovani["accomodation_message_en"],
            "musical_education": self.musical_education if self.musical_education else "-",
            "musical_instrument": self.musical_instrument if self.musical_instrument else "-",
            "repertoire": self.repertoire if self.repertoire else "-",
            "comment": self.comment if self.comment else "-",
            "wants_meals": self.meals,
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
            "tutor_bank_account": self.tutor_bank_account if self.tutor_bank_account else "-",
            "must_change_password_upon_login": "Yes" if self.must_change_password_upon_login else "No",
            "confirmed_email": "Yes" if self.confirmed_email else "No",
            "is_locked": "Yes" if self.is_locked else "No",
            "datetime_created": pretty_datetime(self.datetime_created),
            "parent": self.parent.get_full_name("en") if self.parent else "-",
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name("en")
                } for child in self.children
            ] if len(self.children) > 0 else "-",
        }
        
        
    def info_pro_user_upravu(self) -> dict:
        zmena_ucasti = "povolena"
        if any([self.primary_class, self.secondary_classes]):
            zmena_ucasti = "zakázána"
            
        zmena_kategorie = "povolena"
        tridy = []
        if self.primary_class:
            tridy.append(self.primary_class)
        for t in self.secondary_classes:
            tridy.append(t)
        for trida in tridy:
            if trida.age_group != "both":
                zmena_kategorie = "zakázána"
                break
        
        return {
            "name": self.name if self.name else "",
            "surname": self.surname if self.surname else "",
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self.date_of_birth.strftime("%Y-%m-%d") if self.date_of_birth else None,
            "is_student": "Ano" if self.is_student else "Ne",
            "zmena_kategorie": zmena_kategorie,
            "age_category": "child" if self.is_under_16 else "adult",
            "zmena_letosni_ucasti": zmena_ucasti, # zmena aaktivni a pasivni je take podminena zadnejma tridama
            "is_this_year_participant": "Ano" if self.is_this_year_participant else "Ne",
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "active" if self.is_active_participant else "passive",
            "zmena_ucasti": zmena_ucasti,
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "zmena_ubytka": zmena_ucasti,
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
            "manager_name": self.parent.get_full_name("cz") if self.parent else "",
            "tutor_travel": self.tutor_travel,
            "tutor_license_plate": self.tutor_license_plate,
            "tutor_arrival": self.tutor_arrival,
            "tutor_departure": self.tutor_departure,
            "tutor_accompanying_names": self.tutor_accompanying_names,
            "tutor_address": self.tutor_address,
            "tutor_bank_account": self.tutor_bank_account,
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name("cz")
                } for child in self.children
            ]
        }   
        
        
    def info_pro_en_user_upravu(self) -> dict: # stejny jako cz verze, ale z duvodu konsistence to tu nechavam zalozene
        zmena_ucasti = "povolena"
        if any([self.primary_class, self.secondary_classes]):
            zmena_ucasti = "zakázána"
            
        zmena_kategorie = "povolena"
        tridy = []
        if self.primary_class:
            tridy.append(self.primary_class)
        for t in self.secondary_classes:
            tridy.append(t)
        for trida in tridy:
            if trida.age_group != "both":
                zmena_kategorie = "zakázána"
                break
        
        return {
            "name": self.name if self.name else "",
            "surname": self.surname if self.surname else "",
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self.date_of_birth.strftime("%Y-%m-%d") if self.date_of_birth else None,
            "is_student": "Ano" if self.is_student else "Ne",
            "zmena_kategorie": zmena_kategorie,
            "age_category": "child" if self.is_under_16 else "adult",
            "zmena_letosni_ucasti": zmena_ucasti, # zmena aaktivni a pasivni je take podminena zadnejma tridama
            "is_this_year_participant": "Ano" if self.is_this_year_participant else "Ne",
            "is_ssh_member": "Ano" if self.is_ssh_member else "Ne",
            "is_active_participant": "active" if self.is_active_participant else "passive",
            "zmena_ucasti": zmena_ucasti,
            "is_student_of_partner_zus": "Ano" if self.is_student_of_partner_zus else "Ne",
            "zmena_ubytka": zmena_ucasti,
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
            "manager_name": self.parent.get_full_name("en") if self.parent else "",
            "tutor_travel": self.tutor_travel,
            "tutor_license_plate": self.tutor_license_plate,
            "tutor_arrival": self.tutor_arrival,
            "tutor_departure": self.tutor_departure,
            "tutor_accompanying_names": self.tutor_accompanying_names,
            "tutor_address": self.tutor_address,
            "tutor_bank_account": self.tutor_bank_account,
            "children": [
                {
                    "id": child.id,
                    "full_name": child.get_full_name("en")
                } for child in self.children
            ]
        }  
    
    
    def nacist_zmeny_z_user_requestu(self, request):
        self.name = request.form.get("name")
        self.surname = request.form.get("surname")
        self.phone = request.form.get("phone")
        self.date_of_birth = datetime.strptime(request.form.get("date_of_birth"), "%Y-%m-%d") if request.form.get("date_of_birth") else None
        self.is_student = True if request.form.get("is_student") == "Ano" else False
        self.is_under_16 = True if request.form.get("age_category") == "child" else False
        self.is_this_year_participant = True if request.form.get("is_this_year_participant") == "Ano" else False
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
        self.tutor_bank_account = request.form.get("tutor_bank_account")
        
        if request.form.get("new_password"):
            self.password = generate_password_hash(request.form.get("new_password"), method="scrypt")
        # parent_email je vyresenej ve view
        # zmena e-mailu je taky ve view
        
        self.update()
        
    
    def get_age(self) -> str:
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return str(age)
        else:
            return "-"
        

    def info_for_tutor(self) -> dict:
        return {
            "full_name_cz": self.get_full_name("cz"),
            "full_name_en": self.get_full_name("en"),
            "email": self.email if self.email else "-",
            "phone": self.phone if self.phone else "-",
            "age": self.get_age() ,
            "education": self.musical_education if self.musical_education else "-",
            "repertoire": self.repertoire if self.repertoire else "-",
            "instrument": self.musical_instrument if self.musical_instrument else "-",
            "datetime_class_pick": pretty_datetime(self.datetime_class_pick) if self.datetime_class_pick else "-",
        }
        
    
    def info_for_calculation_email(self) -> dict:
        settings = get_settings()
        return {
            "rok": datetime.now().year,
            "url": url_for("user_views.account", _external=True),
            "celkova_castka": pretty_penize(self.kalkulace()["celkem"], self.billing_currency), 
            "bank_account": settings["czk_bank_account"] if self.billing_currency == "czk" else settings["eur_bank_account"],
            "iban": settings["czk_iban"] if self.billing_currency == "czk" else settings["eur_iban"],
            "swift": settings["czk_swift"] if self.billing_currency == "czk" else settings["eur_swift"],
            "bic": settings["czk_bic"] if self.billing_currency == "czk" else settings["eur_bic"],
            "address": settings["czk_address"] if self.billing_currency == "czk" else settings["eur_address"],
            "zprava_pro_prijemce": self.get_full_name("cz")
            
        }
    
    
    def info_for_en_calculation_email(self) -> dict:
        settings = get_settings()
        return {
            "rok": datetime.now().year,
            "url": url_for("user_views.en_account", _external=True),
            "celkova_castka": pretty_penize(self.kalkulace()["celkem"], self.billing_currency), 
            "bank_account": settings["czk_bank_account"] if self.billing_currency == "czk" else settings["eur_bank_account"],
            "iban": settings["czk_iban"] if self.billing_currency == "czk" else settings["eur_iban"],
            "swift": settings["czk_swift"] if self.billing_currency == "czk" else settings["eur_swift"],
            "bic": settings["czk_bic"] if self.billing_currency == "czk" else settings["eur_bic"],
            "address": settings["czk_address"] if self.billing_currency == "czk" else settings["eur_address"],
            "zprava_pro_prijemce": self.get_full_name("en")
        }
    

    @staticmethod
    def vytvorit_seznam(kriteria: dict) -> dict:
        print("kriteria", kriteria)
        
        ucastnici: list[User] = User.get_all()
        
        # odstranim vsechny s roli
        ucastnici = list(filter(lambda u: len(u.roles) == 0, ucastnici))
        
        
        # mnozina
        if kriteria["mnozina"] == "all":
            pass
        elif kriteria["mnozina"] == "enrolled":
            ucastnici = list(filter(lambda u: u.primary_class_id, ucastnici))
        elif kriteria["mnozina"] == "interested":
            ucastnici = list(filter(lambda u: u.is_this_year_participant, ucastnici))
        
        # filtr tříd
        if len(kriteria["tridy"]) != 0:
            ucastnici_temp = ucastnici
            ucastnici = []
            for u in ucastnici_temp:
                tridy_ids = [c.id for c in u.secondary_classes]
                tridy_ids.append(u.primary_class_id)
                for class_id in tridy_ids:
                    if class_id in kriteria["tridy"]:
                        ucastnici.append(u)
                        break
            
        #filtr ubytka
        if len(kriteria["ubytko"]) != 0:
            ucastnici = list(filter(lambda u: u.accomodation_type in kriteria["ubytko"], ucastnici))
            
        # filtr stravy
        if len(kriteria["strava"]) != 0:
            u_snidane_zs = []
            u_snidane_vs = []
            u_obed_zs = []
            u_obed_vs = []
            u_vecere_zs = []
            u_vecere_vs = []
            if "snidane_zs" in kriteria["strava"]:
                for u in ucastnici:
                    for mo in u.meal_orders:
                        if mo.meal.type == "breakfast" and mo.meal.location == "zs":
                            u_snidane_zs.append(u)
                            break
            if "snidane_vs" in kriteria["strava"]:
                for u in ucastnici:
                    for mo in u.meal_orders:
                        if mo.meal.type == "breakfast" and mo.meal.location == "vs":
                            u_snidane_vs.append(u)
                            break
            if "obed_zs" in kriteria["strava"]:
                for u in ucastnici:
                    for mo in u.meal_orders:
                        if mo.meal.type == "lunch" and mo.meal.location == "zs":
                            u_obed_zs.append(u)
                            break
            if "obed_vs" in kriteria["strava"]:
                for u in ucastnici:
                    for mo in u.meal_orders:
                        if mo.meal.type == "lunch" and mo.meal.location == "vs":
                            u_obed_vs.append(u)
                            break
            if "vecere_zs" in kriteria["strava"]:
                for u in ucastnici:
                    for mo in u.meal_orders:
                        if mo.meal.type == "dinner" and mo.meal.location == "zs":
                            u_vecere_zs.append(u)
                            break
            if "vecere_vs" in kriteria["strava"]:
                for u in ucastnici:
                    for mo in u.meal_orders:
                        if mo.meal.type == "dinner" and mo.meal.location == "vs":
                            u_vecere_vs.append(u)
                            break
                        
            ucastnici = list(set(u_snidane_zs + u_snidane_vs + u_obed_zs + u_obed_vs + u_vecere_zs + u_vecere_vs))
        
        # filtr ostatnich
        if "korekce" in kriteria["ostatni"]:
            ucastnici = list(filter(lambda u: u.billing_correction + u.billing_food_correction + u.billing_accomodation_correction != 0, ucastnici))
        if "neregistrace" in kriteria["ostatni"]:
            ucastnici = list(filter(lambda u: not u.datetime_registered, ucastnici))
        if "dar" in kriteria["ostatni"]:
            ucastnici = list(filter(lambda u: u.billing_gift != 0, ucastnici))
        if "poznamka" in kriteria["ostatni"]:
            ucastnici = list(filter(lambda u: u.comment, ucastnici))
        if "chybejici_udaje" in kriteria["ostatni"]:
            ucastnici_temp = ucastnici
            ucastnici = []
            for u in ucastnici_temp:
                if u.parent:
                    if u.is_this_year_participant and (u.primary_class or not u.is_active_participant) and (not u.name or not u.surname or not u.date_of_birth):
                        ucastnici.append(u)
                else:
                    if u.is_this_year_participant and (u.primary_class or not u.is_active_participant) and (not u.name or not u.surname or not u.email or not u.phone or not u.date_of_birth):
                        ucastnici.append(u)
        if "chybejici_hlavni_trida" in kriteria["ostatni"]:
            ucastnici = list(filter(lambda u: u.secondary_classes and not u.primary_class, ucastnici))
        
        # serazeni
        ucastnici = sorted(ucastnici, key=lambda u: czech_sort.key(u.get_full_name()))
        if kriteria["atribut_razeni"] == "surname":
            ucastnici = sorted(ucastnici, key=lambda u: czech_sort.key(u.surname if u.surname else ""))
        elif kriteria["atribut_razeni"] == "name":
            ucastnici = sorted(ucastnici, key=lambda u: czech_sort.key(u.name if u.name else ""))
        elif kriteria["atribut_razeni"] == "datetime_created":
            ucastnici = sorted(ucastnici, key=lambda u: u.datetime_created if u.datetime_created else datetime(1, 1, 1))
        elif kriteria["atribut_razeni"] == "datetime_class_pick":
            ucastnici = sorted(ucastnici, key=lambda u: u.datetime_class_pick if u.datetime_class_pick else datetime(1, 1, 1)) 
        elif kriteria["atribut_razeni"] == "datetime_registered":
            ucastnici = sorted(ucastnici, key=lambda u: u.datetime_registered if u.datetime_registered else datetime(1, 1, 1))
        elif kriteria["atribut_razeni"] == "age":
            ucastnici = sorted(ucastnici, key=lambda u: int(u.get_age()) if u.date_of_birth else 0)
        elif kriteria["atribut_razeni"] == "billing_date_paid":
            ucastnici = sorted(ucastnici, key=lambda u: u.billing_date_paid if u.billing_date_paid else date(1, 1, 1))
        elif kriteria["atribut_razeni"] == "billing_total":
            ucastnici = sorted(ucastnici, key=lambda u: u.kalkulace()["celkem"])
        elif kriteria["atribut_razeni"] == "billing_gift":
            ucastnici = sorted(ucastnici, key=lambda u: u.billing_gift)
        elif kriteria["atribut_razeni"] == "billing_currency":
            ucastnici = sorted(ucastnici, key=lambda u: u.billing_currency)
        elif kriteria["atribut_razeni"] == "is_ssh_member":
            ucastnici = sorted(ucastnici, key=lambda u: u.is_ssh_member)
        elif kriteria["atribut_razeni"] == "is_active_participant":
            ucastnici = sorted(ucastnici, key=lambda u: u.is_active_participant)
        elif kriteria["atribut_razeni"] == "accomodation_type":
            ucastnici = sorted(ucastnici, key=lambda u: u.accomodation_type if u.accomodation_type else "")
        elif kriteria["atribut_razeni"] == "is_student_of_partner_zus":
            ucastnici = sorted(ucastnici, key=lambda u: u.is_student_of_partner_zus)
        
        # vypsani atribut
        result = {
            "emaily":"",
            "lidi": [],
            "headers": []
        }
        for i, u in enumerate(ucastnici):
            entry = {
                "#": i+1,
                "Jméno": u.get_full_name(),
            }
            result["headers"] = ["#", "Jméno"]
            for a in kriteria["atributy"]:
                # osobni
                if a == "cas":
                    entry["Čas vyplnění přihlášky"] = pretty_datetime(u.cas)
                    result["headers"].append("Čas vyplnění přihlášky")
                elif a == "date_of_birth":
                    entry["Datum narození"] = pretty_date(u.date_of_birth) if u.date_of_birth else "-"
                    result["headers"].append("Datum narození")
                elif a == "age":
                    entry["Věk"] = u.get_age()
                    result["headers"].append("Věk")
                elif a == "email":
                    entry["Email"] = u.email
                    result["headers"].append("E-mail")
                elif a == "phone":
                    entry["Telefon"] = u.phone
                    result["headers"].append("Telefon")
                elif a == "is_student":
                    entry["Student"] = "ano" if u.is_student else "ne"
                    result["headers"].append("Student")
                elif a == "is_under_16":
                    entry["Je pod 16 let?"] = "ano" if u.is_under_16 else "ne"
                    result["headers"].append("Je pod 16 let?")
                    
                # casy
                elif a == "datetime_created":
                    entry["Čas vytvoření účtu"] = pretty_datetime(u.datetime_created)
                    result["headers"].append("Čas vytvoření účtu")
                elif a == "datetime_class_pick":
                    entry["Čas výběru hlavní třídy"] = pretty_datetime(u.datetime_class_pick)
                    result["headers"].append("Čas výběru hlavní třídy")
                elif a == "datetime_registered":
                    entry["Čas registrace ve Valticích"] = pretty_datetime(u.datetime_registered)
                    result["headers"].append("Čas registrace ve Valticích")
                elif a == "datetime_calculation_email":
                    entry["Čas odeslání kalkulace"] = pretty_datetime(u.datetime_calculation_email)
                    result["headers"].append("Čas odeslání kalkulace")
                elif a == "billing_date_paid":
                    entry["Datum zaplacení"] = pretty_datetime(u.billing_date_paid)
                    result["headers"].append("Datum zaplacení")
                    
                # valtice           
                elif a == "is_this_year_participant":
                    entry["Je letošním účastníkem?"] = "ano" if u.is_this_year_participant else "ne"
                    result["headers"].append("Je letošním účastníkem?")
                elif a == "is_ssh_member":
                    entry["Člen SSH?"] = "ano" if u.is_ssh_member else "ne"
                    result["headers"].append("Člen SSH?")
                elif a == "is_active_participant":
                    entry["Účast"] = "aktivní" if u.is_active_participant else "pasivní"
                    result["headers"].append("Účast")
                elif a == "is_student_of_partner_zus":
                    entry["Student ZUŠ Valtice/Mikulov?"] = "ano" if u.is_student_of_partner_zus else "ne"
                    result["headers"].append("Student ZUŠ Valtice/Mikulov?")
                elif a == "accomodation_type":
                    entry["Typ ubytování"] = "internát" if u.accomodation_type == "vs" else "tělocvična" if u.accomodation_type == "gym" else "vlastní" if u.accomodation_type == "own" else "-"
                    result["headers"].append("Typ ubytování")
                elif a == "accomodation_count":
                    entry["Počet lůžek"] = u.accomodation_count
                    result["headers"].append("Počet lůžek")
                elif a == "musical_education":
                    entry["Hudební vzdělání"] = u.musical_education
                    result["headers"].append("Hudební vzdělání")
                elif a == "musical_instrument":
                    entry["Hudební nástroj"] = u.musical_instrument
                    result["headers"].append("Hudební nástroj")
                elif a == "repertoire":
                    entry["Repertoár"] = u.repertoire
                    result["headers"].append("Repertoár")
                elif a == "comment":
                    entry["Uživatelská poznámka"] = u.comment
                    result["headers"].append("Uživatelská poznámka")
                elif a == "admin_comment":
                    entry["Organizátorská poznámka"] = u.admin_comment
                    result["headers"].append("Organizátorská poznámka")
                elif a == "meals":
                    entry["Strava"] = u.get_meals_top_visible()
                    result["headers"].append("Strava")
                
                # finance
                elif a == "billing_currency":
                    entry["Měna"] = u.billing_currency
                    result["headers"].append("Měna")
                elif a == "billing_total":
                    entry["Celkem"] = u.kalkulace()["celkem"]
                    result["headers"].append("Celkem")
                elif a == "billing_gift":
                    entry["Dar"] = u.billing_gift
                    result["headers"].append("Dar")
                elif a in ["billing_total", "billing_classes", "billing_meals", "billing_accomodation"]:
                    k = u.kalkulace()
                    if a == "billing_total":
                        entry["Celkem"] = k["celkem"]
                        result["headers"].append("Celkem")
                    elif a == "billing_classes":
                        entry["Kurzovné"] = k["hlavni_trida"] if k["hlavni_trida"] else 0 + sum(k["vedlejsi_tridy"])
                        result["headers"].append("Kurzovné")
                    elif a == "billing_meals":
                        entry["Strava"] = k["snidane"] + k["obedy"] + k["vecere"] if u.meals else 0
                        result["headers"].append("Strava")
                    elif a == "billing_accomodation":
                        entry["Ubytování"] = k["ubytovani"]
                        result["headers"].append("Ubytování")
                elif a == "billing_correction":
                    entry["Korekce"] = u.billing_correction
                    result["headers"].append("Korekce")
                elif a == "billing_correction_reason":
                    entry["Důvod korekce"] = u.billing_correction_reason
                    result["headers"].append("Důvod korekce")
                elif a == "billing_food_correction":
                    entry["Korekce stravy"] = u.billing_food_correction
                    result["headers"].append("Korekce stravy")
                elif a == "billing_food_correction_reason":
                    entry["Důvod korekce stravy"] = u.billing_food_correction_reason
                    result["headers"].append("Důvod korekce stravy")
                elif a == "billing_accomodation_correction":
                    entry["Korekce ubytování"] = u.billing_accomodation_correction
                    result["headers"].append("Korekce ubytování")
                elif a == "billing_accomodation_correction_reason":
                    entry["Důvod korekce ubytování"] = u.billing_accomodation_correction_reason
                    result["headers"].append("Důvod korekce ubytování")
                
                # přístupy
                elif a == "must_change_password_upon_login":
                    entry["Změna hesla po přihlášení"] = "ano" if u.must_change_password_upon_login else "ne"
                    result["headers"].append("Změna hesla po přihlášení")
                elif a == "confirmed_email":
                    entry["Potvrzený e-mail"] = "ano" if u.confirmed_email else "ne"
                    result["headers"].append("Potvrzený e-mail")
                elif a == "is_locked":
                    entry["Zamčený účet"] = "ano" if u.is_locked else "ne"
                    result["headers"].append("Zamčený účet")
                elif a == "parent":
                    entry["Nadřazený účet"] = u.parent.get_full_name() if u.parent else "-"
                    result["headers"].append("Nadřazený účet")
                elif a == "children":
                    entry["Podřazené účty"] = ", ".join([child.get_full_name() for child in u.children]) if len(u.children) > 0 else "-"
                    result["headers"].append("Podřazené účty")
                
                # třídy
                elif a == "primary_class":
                    entry["Hlavní třída"] = u.primary_class.full_name_cz if u.primary_class else "-"
                    result["headers"].append("Hlavní třída")
                elif a == "secondary_classes":
                    entry["Vedlejší třídy"] = ", ".join([trida.full_name_cz for trida in sorted(u.secondary_classes, key=lambda x: czech_sort.key(x.full_name_cz))]) if u.secondary_classes else "-"
                    result["headers"].append("Vedlejší třídy")
                
            result["lidi"].append(entry)
        seen = set()
        ordered_unique_emails = []
        for u in ucastnici:
            if u.email not in seen:
                ordered_unique_emails.append(u.email)
                seen.add(u.email)
                
        if None in ordered_unique_emails:
            ordered_unique_emails.remove(None)
            
        result["emaily"] = ", ".join(ordered_unique_emails)
        return result

    def vytvorit_xlsx_seznam(kriteria) -> BytesIO:
        data = User.vytvorit_seznam(kriteria)
        wb = Workbook()
        ws = wb.active
        ws.title = "Učastníci"
        keys = data["lidi"][0].keys()
        ws.append(list(keys))
        for radek in data["lidi"]:
            ws.append([radek[k] for k in keys])
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output