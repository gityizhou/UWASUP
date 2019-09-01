import unittest

from recorder import create_app, db
from recorder.models.teacher import Teacher


class TestTeacher(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.teacher = Teacher(staff_number="22302319",
                               first_name="Yi",
                               last_name="Zhou",
                               email="22302319@student.uwa.edu.au",
                               password_hash="admin")
        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        # with self.app.app_context():
        #     db.session.remove()
        #     db.drop_all()
        pass

    def test_teacher_create(self):
        self.teacher.set_password("admin")
        self.teacher.add()
        checkteacher = db.session.query(Teacher).filter(Teacher.id == '1').one()
        self.assertEqual(checkteacher, self.teacher)

    def test_teacher_update(self):
        self.teacher.add()
        checkteacher = db.session.query(Teacher).filter(Teacher.id == '1').one()
        checkteacher.teacher_name = "Java"
        checkteacher.update()
        self.assertEqual(checkteacher.teacher_name, "Java")

    def test_teacher_delete(self):
        # self.teacher.add()
        checkteacher = db.session.query(Teacher).filter(Teacher.id == '1').one()
        checkteacher.delete()
