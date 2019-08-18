from recorder import db


class User(db.Model):
    id = None
    student_number = None
    password_hash = None
    records = None

    def __init__(self, student_number, password_hash):
        self.student_number = student_number
        self.password_hash = password_hash

    def __repr__(self):
        return 'id={}, student_number={},password_hash={}'.format(
            self.id, self.student_number, self.password_hash
        )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def set_password(self, password):
        pass

    def check_password(self, password):
        pass

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass


class Record(db.Model):
    id = None
    url = None
    comment = None
    mark = None
    upload_time = None
    owner_id = None

    def __repr__(self):
        return 'id={}, url={},comment={}, mark={},upload_time={},ownerId={},'.format(
            self.id, self.url, self.comment, self.mark, self.upload_time,self.owner_id
        )

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

class Taks(db.Model):
    id = None
    task_name= None
    description = None
    create_time = None
    due_time = None
    unit_id = None

    def __repr__(self):
        return 'id={}, task_name={},description={}, create_time={},due_time={},unit_id={},'.format(
            self.id, self.task_name, self.description, self.create_time, self.due_time, self.unit_id
        )

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass




class Unit(db.Model):
    id = None
    unit_name = None

    def __repr__(self):
        return 'id={}, unit_name={}'.format(
            self.id, self.unit_name
        )

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
