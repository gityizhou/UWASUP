from recorder import db
# from recorder.models.unit import Unit
from recorder.models.user_task import User_task

class User_unit(db.Model):
    __tablename__ = 'user_unit'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), primary_key=True)
    user = db.relationship("User", back_populates="units")
    unit = db.relationship("Unit", back_populates="users")

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # this_unit = db.session.query(Unit).filter(Unit.id == self.unit_id).first()
        # tasks = this_unit.tasks
        # for task in tasks:
        #     User_task.query.filter_by(task_id=task.id, user_id=self.user_id).first().delete()
        tasks = self.unit.tasks
        for task in tasks:
            user_task = User_task.query.filter_by(task_id=task.id, user_id=self.user_id).first()
            if user_task:
                user_task.delete()

        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
