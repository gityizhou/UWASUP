from datetime import datetime
from recorder import db


class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assignment_name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    due_time = db.Column(db.DateTime)
    task = db.relationship("Task")
    # foreign key to unit table
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    students = db.relationship("Student", secondary='student_assignment_link')

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
