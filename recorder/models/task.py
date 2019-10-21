from datetime import datetime
from recorder import db
from recorder.models.user import User
from recorder.models.user_task import User_task
from recorder import route
import os

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(64))
    description = db.Column(db.String(300))
    create_time = db.Column(db.DateTime, default=datetime.now)
    due_time = db.Column(db.DateTime)
    pdf_url = db.Column(db.String(140))
    pdf_id = db.Column(db.String(140))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = db.relationship("Unit", back_populates="tasks")
    questions = db.relationship("Question", back_populates="task")
    users = db.relationship("User_task", back_populates="task")

    def __repr__(self):
        return 'id={}, task_name={},description={}'.format(
            self.id, self.task_name, self.description
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        pdf_id = self.pdf_id
        file = route.drive.CreateFile({'id': pdf_id})
        file.Delete()
        for question in self.questions:
            print(question)
            question.delete()
        user_tasks = db.session.query(User_task).filter(User_task.task_id == self.id )
        for user_task in user_tasks:
            print(user_task.task_id)
            user_task.delete()
        db.session.delete(self)
        db.session.commit()

    def delete_pdf(self):
        pdf_id = self.pdf_id
        file = route.drive.CreateFile({'id': pdf_id})
        file.Delete()
        self.pdf_id = None
        self.pdf_url = None
        self.update()

    def update(self):
        db.session.commit()

    def add_task2unit(self, unit):
        self.unit_id = unit.id
        db.session.commit()

    def get_task_users(self):
        users = []
        for user_task in self.users:
            user_id = user_task.user_id
            users.append(db.session.query(User).filter(User.id == user_id).one())
        return users




