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

    def get_short_name_id_for_seznam(self):
        return {
            "id": self.id,
            "short_name": self.short_name
        }
    
    def get_by_full_name(full_name: str) -> "Valtice_trida":
        return db.session.scalars(db.select(Valtice_trida).where(Valtice_trida.full_name == full_name)).first()
    
    def info_pro_detail(self):
        return {
            "short_name": self.short_name,
            "full_name": self.full_name,
            "hlavni_ucastnici_1": [{"name": u.get_full_name(), "link": "/valtice/ucastnik/" + str(u.id)} for u in self.hlavni_ucastnici_1],
            "hlavni_ucastnici_2": [{"name": u.get_full_name(), "link": "/valtice/ucastnik/" + str(u.id)} for u in self.hlavni_ucastnici_2],
            "vedlejsi_ucastnici_placeni": [{"name": u.get_full_name(), "link": "/valtice/ucastnik/" + str(u.id)} for u in self.vedlejsi_placena_ucastnici],
            "vedlejsi_ucastnici_zdarma": [{"name": u.get_full_name(), "link": "/valtice/ucastnik/" + str(u.id)} for u in self.vedlejsi_zdarma_ucastnici],
            "celkem": len(self.hlavni_ucastnici_1) + len(self.hlavni_ucastnici_2) + len(self.vedlejsi_placena_ucastnici) + len(self.vedlejsi_zdarma_ucastnici),
            "prvni_trida_count": len(self.hlavni_ucastnici_1),
            "druha_trida_count": len(self.hlavni_ucastnici_2),
            "vedlejsi_placena_count": len(self.vedlejsi_placena_ucastnici),
            "vedlejsi_zdarma_count": len(self.vedlejsi_zdarma_ucastnici)
        }