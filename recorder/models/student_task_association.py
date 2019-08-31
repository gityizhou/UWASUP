from recorder import db


class StudentAssignmentAssociation(db.Model):
    __tablename__ = 'student_assignment_link'
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), primary_key=True)
    # comment = db.relationship("Comment")
