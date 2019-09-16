import unittest

from recorder import create_app, db
from recorder.models.student import Student


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.student = Student(student_number="22302319",
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

    def test_student_create(self):
        self.student.set_password("admin")
        self.student.add()
        checkstudent = db.session.query(Student).filter(Student.id == '1').one()
        self.assertEqual(checkstudent, self.student)

    def test_student_update(self):
        self.student.add()
        checkstudent = db.session.query(Student).filter(Student.id == '1').one()
        checkstudent.student_name = "Java"
        checkstudent.update()
        self.assertEqual(checkstudent.student_name, "Java")

    def test_student_delete(self):
        # self.student.add()
        checkstudent = db.session.query(Student).filter(Student.id == '1').one()
        checkstudent.delete()
