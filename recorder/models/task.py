from datetime import datetime
from recorder import db


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(64))
    description = db.Column(db.String(300))
    create_time = db.Column(db.DateTime, default=datetime.now)
    due_time = db.Column(db.DateTime)
    pdf_url = db.String(db.String(64))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = db.relationship("Unit", back_populates="tasks")
    questions = db.relationship("Question", back_populates="task")
    users = db.relationship("User_task", back_populates="task")

    def __repr__(self):
        return 'id={}, task_name={},description={}, create_time={},due_time={},pdf_url={},'.format(
            self.id, self.task_name, self.description, self.create_time, self.due_time, self.pdf_url
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def add_task2unit(self, unit):
        self.unit_id = unit.id
        db.session.commit()
