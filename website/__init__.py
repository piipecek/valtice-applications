import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, current_user
from flask_mail import Mail
from .helpers.check_files import check_data_folder, check_settings_file
from .paths import dotenv_path
from .helpers.settings_manager import is_class_signup_closed, is_secondary_class_signup_open, is_primary_class_signup_open, get_settings

db = SQLAlchemy()
cors = CORS()
mail = Mail()
login_manager = LoginManager()
load_dotenv(dotenv_path=dotenv_path(), verbose=True)


def create_app() -> Flask:
    check_data_folder()
    check_settings_file()
        
    db_driver = os.environ.get("DB_DRIVER")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_address = os.environ.get("DB_ADDRESS")
    db_name = os.environ.get("DB_NAME")
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{db_driver}://{db_username}:{db_password}@{db_address}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_PORT"] = "587"
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    from .views.guest_views import guest_views
    from .views.auth_views import auth_views
    from .views.org_views import org_views
    from .views.user_views import user_views
    from .api.guest_api import guest_api
    from .api.org_api import org_api
    from .api.static_sender import static_sender
    from .api.user_api import user_api


    app.register_blueprint(guest_views, url_prefix="/")
    app.register_blueprint(auth_views, url_prefix="/auth")
    app.register_blueprint(org_views, url_prefix = "/organizator")
    app.register_blueprint(user_views, url_prefix = "/user")
    app.register_blueprint(guest_api, url_prefix = "/guest_api")
    app.register_blueprint(org_api, url_prefix = "/org_api")
    app.register_blueprint(static_sender, url_prefix="/static")
    app.register_blueprint(user_api, url_prefix="/user_api")


    from .models.role import Role
    from .models.user import User
    from .helpers.get_roles import get_roles
    from .models.trida import Trida
    from .models.billing import Billing
    from .models.meal import Meal
    from .models.meal_order import Meal_order
 
    with app.app_context():
        db.create_all()

    login_manager.login_view = "auth_views.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # get rovou kouka na primary key, nemusim delat filter_by(id=id)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("guest/not_found.html", roles=get_roles()), 404

    @app.errorhandler(401)
    def not_authorised(e):
        return render_template("guest/not_authorised.html", roles=get_roles()), 401
    
    @app.context_processor
    def inject_globals():
        cz_lektor_tridy_title = ""
        en_lektor_tridy_title = ""
        if current_user.is_authenticated:
            if len(current_user.taught_classes) <= 1:
                cz_lektor_tridy_title = "Moje třída"
                en_lektor_tridy_title = "My class"
            else:
                cz_lektor_tridy_title = "Moje třídy"
                en_lektor_tridy_title = "My classes"
                
        return dict(
            cz_url = os.environ.get("CZ_HOME_URL"),
            en_url = os.environ.get("EN_HOME_URL"),
            name_cz = current_user.get_full_name("cz") if current_user.is_authenticated else None,
            name_en = current_user.get_full_name("en") if current_user.is_authenticated else None,
            cz_lektor_tridy_title = cz_lektor_tridy_title,
            en_lektor_tridy_title = en_lektor_tridy_title,
            aktivni_ucast = current_user.is_active_participant if current_user.is_authenticated else None,
            is_class_signup_closed = is_class_signup_closed(),
            is_primary_class_signup_open = is_primary_class_signup_open(),
            is_secondary_class_signup_open = is_secondary_class_signup_open(),
            is_under_16 = current_user.is_under_16 if current_user.is_authenticated else None,
            users_can_send_calculations = get_settings()["users_can_send_calculations"],
        )

    return app