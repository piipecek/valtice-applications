from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Valtice_trida(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String(300), nullable=False)
    full_name = db.Column(db.String(1000), nullable=False)
    hlavni_ucastnici_1 = db.relationship('Valtice_ucastnik', backref='hlavni_trida_1', lazy=True, foreign_keys='Valtice_ucastnik.hlavni_trida_1_id')
    hlavni_ucastnici_2 = db.relationship('Valtice_ucastnik', backref='hlavni_trida_2', lazy=True, foreign_keys='Valtice_ucastnik.hlavni_trida_2_id')
    vedlejsi_placena_ucastnici = db.relationship('Valtice_ucastnik', backref='vedlejsi_trida_placena', lazy=True, foreign_keys='Valtice_ucastnik.vedlejsi_trida_placena_id')
    vedlejsi_zdarma_ucastnici = db.relationship('Valtice_ucastnik', backref='vedlejsi_trida_zdarma', lazy=True, foreign_keys='Valtice_ucastnik.vedlejsi_trida_zdarma_id')
