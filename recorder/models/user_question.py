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
    is_submitted = db.Column(db.Integer, default=0)
    question = db.relationship("Question", back_populates="users")
    user = db.relationship("User", back_populates="questions")

    @staticmethod
    def add_user_question(user, question, recorder_url):
        user_has_question = User_question(user=user, question=question, recorder_url=recorder_url)
        db.session.add(user_has_question)
        db.session.commit()


"""
example association:
user_has_question = User_question(user=<someuser>, question=<somequestion>, recorder_url=<url>)
db.session.add(user_has_question)
db.session.commit()

"""
