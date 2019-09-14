import unittest

from recorder import create_app, db
from recorder.models.user import User
from recorder.models.unit import Unit


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        # with self.app.app_context():
        #     db.session.remove()
        #     db.drop_all()
        pass

    def test_user_create(self):
        user1 = User(user_number="24444444",
                     first_name = 'Alex',
                     last_name = 'McAllister',
                     email='24444444@student.uwa.edu.au')
        user1.set_password("admin")
        user1.add()


    def test_student2teacher(self):
        user1 = db.session.query(User).filter(User.id == '3').one()
        user1.student2teacher()


    def test_user_add_unit(self):
        user1 = db.session.query(User).filter(User.id == '3').one()
        unit = db.session.query(Unit).filter(Unit.id == '1').one()
        user1.add_unit(unit)

    def test_user_unit_query(self):
        user1 = db.session.query(User).filter(User.id == '3').one()
        print(user1.units.all())

    def test_user_delete(self):
        # self.student.add()
        user = db.session.query(User).filter(User.id == '1').one()
        user.delete()

