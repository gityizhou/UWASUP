from recorder import db


class User(db.Model):
    id = None
    student_number = None
    password_hash = None
    records = None

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
    owner_id = None

    def __repr__(self):
        return 'id={}, url={},ownerId={}'.format(
            self.id, self.url, self.owner_id
        )

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

