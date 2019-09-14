import unittest

from recorder import create_app, db
from recorder.models.student import Student
from recorder.models.teacher import Teacher

class TestTeacher(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.teacher = Teacher(staff_number="88888888",
                               first_name="Ramond",
                               last_name="He",
                               email="88888888@student.uwa.edu.au")
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
