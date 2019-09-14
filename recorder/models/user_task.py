from recorder import db


class User_task(db.Model):
    __tablename__ = 'user_task'
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    comment = db.Column(db.String(140))
    recorder_url = db.Column(db.String(140))
    task = db.relationship("Task", back_populates="users")
    user = db.relationship("User", back_populates="tasks")
