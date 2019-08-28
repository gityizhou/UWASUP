from datetime import datetime


from recorder import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(128), unique=True, index=True)
    mark = db.Column(db.Float)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    comment_id = db.relationship('Comment', backref='record_comment', lazy='dynamic')
    owner_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __repr__(self):
        return 'id={}, url={},comment={}, mark={},create_time={},ownerId={},'.format(
            self.id, self.url, self.comment, self.mark, self.create_time,self.owner_id
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()