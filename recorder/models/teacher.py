from recorder import db
from werkzeug.security import generate_password_hash, check_password_hash


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_number = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    units = db.relationship("Unit")

    def __repr__(self):
        return f'id={self.id}, teacher_number={self.teacher_number}, first_name={self.first_name}, last_name={self.last_name}, email={self.email},password_hash={self.password_hash}'

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
