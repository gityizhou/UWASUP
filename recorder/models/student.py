from recorder import db
from werkzeug.security import generate_password_hash, check_password_hash
from recorder.models.student_question_association import StudentQuestionAssociation
from recorder.models.student_task_association import StudentTaskAssociation

student_unit_association = db.Table(
    "student_unit_association",
    db.metadata,
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("unit_id", db.Integer, db.ForeignKey("unit.id"), primary_key=True)

)


# student_task_association = db.Table(
#     "student_task_association",
#     db.metadata,
#     db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
#     db.Column("task_id", db.Integer, db.ForeignKey("task.id"), primary_key=True),
#     db.relationship("Record")
# )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_number = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # tasks = db.relationship("Task", backref="student_tasks", secondary=student_task_association)
    tasks = db.relationship("Task", secondary='student_task_link')
    questions = db.relationship("Question", secondary='student_question_link')

    def __repr__(self):
        return f'id={self.id}, student_number={self.student_number}, first_name={self.first_name}, last_name={self.last_name}, email={self.email},password_hash={self.password_hash}'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # encode the password to hash code
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
