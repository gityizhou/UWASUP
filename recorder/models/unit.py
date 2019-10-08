from recorder import db
from recorder.models.user import user_unit

class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_id = db.Column(db.String(20))
    unit_name = db.Column(db.String(64))
    tasks = db.relationship("Task", back_populates="unit")

    def __repr__(self):
        return 'unit_id={}, unit_name={}'.format(
            self.unit_id, self.unit_name
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        for task in self.tasks:
            print(task)
            task.delete()
        # user_units = db.session.query(user_unit).filter(user_unit.c.unit_id == self.id).delete()
        # print(type(user_units))
        # for item in user_units:
        #     print(item)
        #     print(type(item))
        #     db.session.delete(item)
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()







