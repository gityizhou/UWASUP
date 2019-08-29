from recorder import db
from werkzeug.security import generate_password_hash, check_password_hash

association_student_unit = db.Table('association_student_unit', db.Model.metadata,
                                    db.Column('Student', db.Integer, db.ForeignKey('student.id')),
                                    db.Column('Unit', db.Integer, db.ForeignKey('unit.unit_id'))
                                    )


association_student_assignment = db.Table('association_sutdent_assignment', db.Model.metadata,
                                    db.Column('Student', db.Integer, db.ForeignKey('student.id')),
                                    db.Column('Assignment', db.Integer, db.ForeignKey('assignment.id')),
                                          tasks=db.relationship('Task', backref='assignment_tasks', lazy='dynamic')
                                    )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_number = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    units = db.relationship('Unit', secondary=association_student_unit, backref='student_unit_owner', lazy='dynamic')
    assignments = db.relationship('Unit', secondary=association_student_assignment, backref='student_assignment_owner', lazy='dynamic')
    # comments = db.relationship('Comment', backref='owner', lazy='dynamic')
    # records = db.relationship('Record', backref='student_records_owner', lazy='dynamic')

    def __repr__(self):
        return f'id={self.id}, student_number={self.student_number}, first_name={self.first_name}, last_name={self.last_name}, email={self.email},password_hash={self.password_hash}'

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
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    units = db.relationship('Unit', backref='unit_owner', lazy='dynamic')

    # unit = db.relationship('Unit', secondary=association_teacher_unit, backref='teacher_unit_owner', lazy='dynamic')

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
