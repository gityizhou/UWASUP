from recorder import db
from recorder.models.student import student_unit_association


class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_id = db.Column(db.String(20))
    unit_name = db.Column(db.String(64))
    # foreign key to teacher table
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    assignments = db.relationship("Assignment")
    students = db.relationship("Student", backref="unit_students", secondary=student_unit_association)

    def __repr__(self):
        return 'unit_id={}, unit_name={}, teacher_id={}'.format(
            self.unit_id, self.unit_name, self.teacher_id
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
