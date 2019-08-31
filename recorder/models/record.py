from datetime import datetime

from recorder import db


class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(128), unique=True, index=True)
    mark = db.Column(db.Float)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.relationship("Comment")
    student_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    student_question_foreign_key = db.ForeignKeyConstraint(['student_id', 'question_id'],
                                                       ['student_question_link.student_id',
                                                        'student_question_link.task_id'])

    def __repr__(self):
        return 'id={}, url={},comment={}, mark={},create_time={},ownerId={}'.format(
            self.id, self.url, self.comment, self.mark, self.create_time, self.owner_id
        )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
