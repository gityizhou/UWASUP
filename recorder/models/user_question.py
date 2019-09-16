from recorder import db
from datetime import datetime


class User_question(db.Model):
    __tablename__ = 'user_question'
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    recorder_url = db.Column(db.String(140))
    create_time = db.Column(db.DateTime, default=datetime.now)
    question = db.relationship("Question", back_populates="users")
    user = db.relationship("User", back_populates="questions")

    def add_user_question(self, user, question, recorder_url):
        user_has_question = User_question(user=user, question=question, recorder_url=recorder_url)
        db.session.add(user_has_question)
        db.session.commit()
"""
example association:
user_has_question = User_question(user=<someuser>, question=<somequestion>, recorder_url=<url>)
db.session.add(user_has_question)
db.session.commit()

"""
