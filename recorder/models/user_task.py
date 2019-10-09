from recorder import db


class User_task(db.Model):
    __tablename__ = 'user_task'
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    comment = db.Column(db.String(140))
    recorder_url = db.Column(db.String(140))
    mark = db.Column(db.Float)
    task = db.relationship("Task", back_populates="users")
    user = db.relationship("User", back_populates="tasks")

    @staticmethod
    def add_user_task(user, task, comment, mark, recorder_url):
        user_has_task = User_task(user=user, task=task, comment=comment, mark=mark, recorder_url=recorder_url)
        db.session.add(user_has_task)
        db.session.commit()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
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
