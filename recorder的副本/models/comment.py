from recorder import db


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200))
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'))
    student_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    student_task_foreign_key = db.ForeignKeyConstraint(['student_id', 'task_id'],
                                                       ['student_task_link.student_id',
                                                        'student_task_link.assignment_id'])

    def __repr__(self):
        return 'id={}, comment={}'.format(
            self.id, self.comment
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
