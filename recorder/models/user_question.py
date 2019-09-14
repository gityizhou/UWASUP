from recorder import db
from datetime import datetime


class User_question(db.Model):
    __tablename__ = 'user_question'
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    recorder_url = db.Column(db.String(140))
    create_time = db.Column(db.DateTime, default=datetime.now)
    task = db.relationship("Task", back_populates="users")
    user = db.relationship("User", back_populates="tasks")
