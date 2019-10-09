from recorder import db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from recorder.models.question import Question
from recorder.models.user_unit import User_unit
from recorder.models.user_question import User_question
from recorder.models.user_task import User_task
from flask import current_app
import jwt
import time


# user_unit = db.Table('user_unit',
#                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#                      db.Column('unit_id', db.Integer, db.ForeignKey('unit.id'))
#                      )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_number = db.Column(db.String(64), unique=True, index=True)  # student number / staff number
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_teacher = db.Column(db.Integer, default=0)
    is_activated = db.Column(db.Integer, default=0)

    # units = db.relationship('Unit', secondary=user_unit,
    #                         backref=db.backref('users', lazy='dynamic'),
    #                         lazy='dynamic')
    units = db.relationship("User_unit", back_populates="user")
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
        user_units = db.session.query(User_unit).filter(User_unit.user_id == self.id)
        for user_unit in user_units:
            user_unit.delete()
        user_tasks = db.session.query(User_task).filter(User_task.user_id == self.id)
        for user_task in user_tasks:
            user_task.delete()
        user_quesions = db.session.query(User_question).filter(User_question.user_id == self.id)
        for user_quesion in user_quesions:
            # print(user_quesion.question_id)
            user_quesion.delete()
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def student2teacher(self):
        self.is_teacher = 1
        db.session.commit()

    def add_unit(self, unit):
        user_has_unit = User_unit(user=self, unit=unit)
        db.session.add(user_has_unit)
        db.session.commit()

    def delete_unit(self, unit):
        user_has_unit = User_unit(user=self, unit=unit)
        db.session.delete(user_has_unit)
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

    # get the record url of this question of this student
    def get_question_record_url(self, question_id):
        for question in self.questions:
            if question.question_id == question_id:
                return question.record_url

    def get_user_task(self, task_id):
        user = db.session.query(User).filter(User.id == self.id).one()
        for task in user.tasks:
            if task.task_id == task_id:
                return task

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

    def get_jwt(self, expire=3600):
        return jwt.encode(
            {
                'email': self.email,
                'exp': time.time() + expire
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        try:
            email = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            email = email['email']
        except:
            return
        return User.query.filter_by(email=email).first()

    def email_is_verified(self):
        print("===============user email verified===========")
        return


# get the id from session
@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))
