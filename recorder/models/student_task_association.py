from recorder import db


class StudentTaskAssociation(db.Model):
    __tablename__ = 'student_task_link'
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    # record = db.relationship("Record")
