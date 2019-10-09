from recorder import db


class User_unit(db.Model):
    __tablename__ = 'user_unit'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), primary_key=True)
    user = db.relationship("User", back_populates="units")
    unit = db.relationship("Unit", back_populates="users")

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()