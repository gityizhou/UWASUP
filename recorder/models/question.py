from recorder import db


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship("Task", back_populates="questions")
    users = db.relationship("User_question", back_populates="question")

    def __repr__(self):
        return 'id={}, question_name={},description={}'.format(
            self.id, self.question_name, self.description
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def add_question2task(self, task):
        self.task_id = task.id
        db.session.commit()


