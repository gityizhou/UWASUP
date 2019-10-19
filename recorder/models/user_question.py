from recorder import db
from datetime import datetime


class User_question(db.Model):
    __tablename__ = 'user_question'
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    record_url = db.Column(db.String(140))
    record_id = db.Column(db.String(140))
    record_title = db.Column(db.String(140))
    update_time = db.Column(db.DateTime, default=datetime.now)
    question = db.relationship("Question", back_populates="users")
    user = db.relationship("User", back_populates="questions")

    @staticmethod
    def add_user_question(user, question, record_url, record_id, record_title):
        user_has_question = User_question(user=user, question=question, record_url=record_url, record_id=record_id,
                                          record_title=record_title)
        db.session.add(user_has_question)
        db.session.commit()


    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


"""
example association:
user_has_question = User_question(user=<someuser>, question=<somequestion>, recorder_url=<url>)
db.session.add(user_has_question)
db.session.commit()

"""
