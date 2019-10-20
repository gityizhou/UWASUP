from recorder import db
# from recorder.models.task import Task
from recorder.models.user_question import User_question

class User_task(db.Model):
    __tablename__ = 'user_task'
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    comment = db.Column(db.String(140))
    record_url = db.Column(db.String(140))
    record_id = db.Column(db.String(140))
    record_title = db.Column(db.String(140))
    mark = db.Column(db.Float)
    task = db.relationship("Task", back_populates="users")
    user = db.relationship("User", back_populates="tasks")

    @staticmethod
    def add_user_task(user, task):
        user_has_task = User_task(user=user, task=task)
        db.session.add(user_has_task)
        db.session.commit()

    # @staticmethod
    # def get_user_task(user_id, task_id):
    #     user = db.session.query(User).filter(User.id == user_id).one()
    #     for task in user.tasks:
    #         if task.task_id == task_id:
    #             print(task.mark)
    #             return task

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # this_task = db.session.query(Task).filter(Task.id == self.task_id).first()
        # questions = this_task.tasks
        # for question in questions:
        #     User_question.query.filter_by(question_id=question.id, user_id=self.user_id).first().delete()
        questions = self.task.questions
        for question in questions:
            user_question = User_question.query.filter_by(question_id=question.id, user_id=self.user_id).first()
            if user_question:
                user_question.delete()
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


"""
example association:
user_has_task = User_task(user=<someuser>, task=<sometask>, comment="......", recorder_url=<url>)
db.session.add(user_has_task)
db.session.commit()

"""
