from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from website.helpers.pretty_date import pretty_datetime
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_login import UserMixin, current_user, login_user
from typing import List
import jwt

class Valtice_ucastnik(Common_methods_db_model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    cas = db.Column(db.DateTime, default=datetime.utcnow)
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