from recorder import db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from recorder.models.question import Question

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
        return 'id={}, user_number={}, first_name={}, last_name={}, email={},password_hash={}, is_teacher={}'.format(
            self.id, self.user_number, self.first_name, self.last_name, self.email, self.password_hash, self.is_teacher
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

    def student2teacher(self):
        self.is_teacher = 1
        db.session.commit()

    def add_unit(self, unit):
        self.units.append(unit)
        db.session.commit()

    def delete_unit(self, unit):
        self.units.remove(unit)
        db.session.commit()

    # you can use this method to get all questions in this task of a student
    def get_task_questions(self, task_id):
        task_questions = []
        for question in self.questions:
            # print(question.question_id)
            this_question = db.session.query(Question).filter(Question.id == question.question_id).first()
            # print(this_question)
            if this_question.task_id == task_id:
                task_questions.append(this_question)
        return task_questions

    # you can use this method to get the mark of the task of a student of a specific task
    def get_task_mark(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task.mark

    @staticmethod
    def get_user_list():
        return db.session.query(User).all()

    @staticmethod
    def get_by_user_number(usernumber):
        return db.session.query(User).filter(
            User.user_number == usernumber
        ).first()

    @staticmethod
    def get_by_id(user_id):
        return db.session.query(User).filter(
            User.id == user_id
        ).first()

    @staticmethod
    def get_user_list():
        return db.session.query(User).all()

    @staticmethod
    def authenticate(username, password):
        user = User.get_by_username(username)
        if user:
            # check password
            if user.check_password(password):
                return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        user = User.get_by_id(user_id)
        return user


# get the id from session
@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))
