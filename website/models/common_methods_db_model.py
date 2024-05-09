from website import db

class Common_methods_db_model(db.Model):
    __abstract__ = True
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    @classmethod
    def get_all(cls):
        return db.session.scalars(db.select(cls)).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.add(self)
        db.session.commit()
