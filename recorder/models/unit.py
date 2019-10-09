from recorder import db
from recorder.models.user_unit import User_unit


class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_id = db.Column(db.String(20))
    unit_name = db.Column(db.String(64))
    tasks = db.relationship("Task", back_populates="unit")
    users = db.relationship("User_unit", back_populates="unit")

    def __repr__(self):
        return 'unit_id={}, unit_name={}'.format(
            self.unit_id, self.unit_name
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        for task in self.tasks:
            # print(task)
            task.delete()
        user_units = db.session.query(User_unit).filter(User_unit.unit_id == self.id )
        for user_unit in user_units:
            user_unit.delete()
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
