import datetime

from sqlalchemy import DateTime

from recorder import db
from werkzeug.security import generate_password_hash, check_password_hash


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_number = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    comments = db.relationship("Comment")
    records = None

    def __repr__(self):
        return 'id={}, student_number={},email={},password_hash={}'.format(
            self.id, self.student_number, self.email, self.password_hash
        )

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


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_number = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    unit = None

    def __repr__(self):
        return 'id={}, student_number={},email={},password_hash={}'.format(
            self.id, self.student_number, self.email, self.password_hash
        )

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


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(128), unique=True, index=True)
    mark = db.Column(db.Float)
    create_time = db.Column(DateTime, default=datetime.datetime.utcnow)
    comment = None
    owner_id = None

    def __repr__(self):
        return 'id={}, url={},comment={}, mark={},create_time={},ownerId={},'.format(
            self.id, self.url, self.comment, self.mark, self.create_time,self.owner_id
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name= db.Column(db.String(64))
    description = db.Column(db.String(200))
    create_time = db.Column(DateTime, default=datetime.datetime.utcnow)
    due_time = db.Column(DateTime)
    unit_id = None

    def __repr__(self):
        return 'id={}, task_name={},description={}, create_time={},due_time={},unit_id={},'.format(
            self.id, self.task_name, self.description, self.create_time, self.due_time, self.unit_id
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()



class Unit(db.Model):
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(64))
    teacher_id = None


    def __repr__(self):
        return 'id={}, unit_name={}'.format(
            self.id, self.unit_name
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200))

    def __repr__(self):
        return 'id={}, comment={}'.format(
            self.id, self.comment
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
