from recorder import db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

user_unit = db.Table('user_unit',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('unit_id', db.Integer, db.ForeignKey('unit.id'))
                     )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_number = db.Column(db.String(64), unique=True, index=True)  # student number / staff number
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_teacher = db.Column(db.Integer, default=0)

    units = db.relationship('Unit', secondary=user_unit,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')
    tasks = db.relationship("User_task", back_populates="user")
    questions = db.relationship("User_question", back_populates="user")

    def __repr__(self):
        return f'id={self.id}, user_number={self.user_number}, first_name={self.first_name}, last_name={self.last_name}, email={self.email},password_hash={self.password_hash}, is_teacher={self.is_teacher} '

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # encode the password to hash code
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def student2teacher(self):
        self.is_teacher = 1
        db.session.commit()

    def add_unit(self, unit):
        self.units.append(unit)
        db.session.commit()

    def delete_unit(self, unit):
        self.units.remove(unit)
        db.session.commit()



# get the id from session
@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))
