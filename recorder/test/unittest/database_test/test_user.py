import unittest

from recorder import create_app, db
from recorder.models.user import User
from recorder.models.unit import Unit
from recorder.models.task import Task
from recorder.models.question import Question
from recorder.models.user_task import User_task
from recorder.models.user_question import User_question


class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        # will delete all data after each test
        # with self.app.app_context():
        #     db.session.remove()
        #     db.drop_all()
        pass

    # add users
    def test_user_create(self):
        user1 = User(user_number="24444444",
                     first_name='Alex',
                     last_name='McAllister',
                     email='24444444@student.uwa.edu.au')
        user1.set_password("admin")
        user1.add()

    # convert student to teacher
    def test_student2teacher(self):
        user1 = db.session.query(User).filter(User.id == '3').one()
        user1.student2teacher()

    # user select a unit
    def test_user_add_unit(self):
        user1 = db.session.query(User).filter(User.id == '1').one()
        unit = db.session.query(Unit).filter(Unit.id == '1').one()
        user1.add_unit(unit)

    # query user's units
    def test_user_unit_query(self):
        user1 = db.session.query(User).filter(User.id == '3').one()
        print(user1.units.all())

    # add a user's task result
    def test_add_user_task(self):
        task = db.session.query(Task).filter(Task.id == '1').one()
        user1 = db.session.query(User).filter(User.id == '1').one()
        comment = "well done"
        record_url = "www.google.com"
        user_has_task = User_task(user=user1, task=task, comment=comment, recorder_url=record_url)
        db.session.add(user_has_task)
        db.session.commit()

    # user answer his question
    def test_add_user_question(self):
        user1 = db.session.query(User).filter(User.id == '1').one()
        question = db.session.query(Question).filter(Question.id == '5').one()
        record_url = "www.google.com"
        user_has_question = User_question(user=user1, question=question, recorder_url=record_url)
        db.session.add(user_has_question)
        db.session.commit()

    # update user
    def test_user_update(self):
        user = db.session.query(User).filter(User.id == '1').one()
        user.first_name = "testtesttest"
        user.update()

    # delete a user
    def test_user_delete(self):
        # self.student.add()
        user = db.session.query(User).filter(User.id == '1').one()
        user.delete()

    def test_task_mark(self):
        user = db.session.query(User).filter(User.id == '1').one()
        print(user.get_task_mark(1))


    def test_get_task_question(self):
        user = db.session.query(User).filter(User.id == '1').one()
        print(user.get_task_questions(1))