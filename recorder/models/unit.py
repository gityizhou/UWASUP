from recorder import db


class Unit(db.Model):
    unit_id = db.Column(db.String(20), primary_key=True)
    unit_name = db.Column(db.String(64))
    task = db.relationship('Task', backref='unit_task_owner', lazy='dynamic')
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

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