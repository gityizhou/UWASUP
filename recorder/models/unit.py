from recorder import db


class Unit(db.Model):
    unit_id = db.Column(db.String(20), primary_key=True)
    unit_name = db.Column(db.String(64))
    task = db.relationship('Task', backref='unit_task_owner', lazy='dynamic')

    def __repr__(self):
        return 'unit_id={}, unit_name={}'.format(
            self.unit_id, self.unit_name
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()