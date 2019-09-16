from recorder import db


class StudentQuestionAssociation(db.Model):
    __tablename__ = 'student_question_link'
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    # record = db.relationship("Record")
