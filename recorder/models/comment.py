from recorder import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200))
    # student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'))
    # student_id = db.relationship('Student', backref='owner', lazy='dynamic')
    # record_id = db.relationship('Record', backref='owner', lazy='dynamic')

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
