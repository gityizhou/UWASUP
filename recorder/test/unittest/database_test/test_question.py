import unittest

from recorder import create_app, db
from recorder.models.task import Task
from recorder.models.question import Question


class TestQuestion(unittest.TestCase):


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

    def test_question_create(self):
        question1 = Question(question_name="1st essay", description="write your first essay")
        question2 = Question(question_name="2nd essay", description="write your second essay")
        question3 = Question(question_name="3rd essay", description="write your third essay")
        question4 = Question(question_name="4th essay", description="write your forth essay")
        question5 = Question(question_name="5th essay", description="write your fifth essay")
        question1.add()
        question2.add()
        question3.add()
        question4.add()
        question5.add()

    def test_addquestions2task(self):
        task = db.session.query(Task).filter(Task.id == '1').one()
        question1 = db.session.query(Question).filter(Question.id == '1').one()
        question2 = db.session.query(Question).filter(Question.id == '2').one()
        question3 = db.session.query(Question).filter(Question.id == '3').one()
        question4 = db.session.query(Question).filter(Question.id == '4').one()
        question5 = db.session.query(Question).filter(Question.id == '5').one()
        question1.add_question2task(task)
        question2.add_question2task(task)
        question3.add_question2task(task)
        question4.add_question2task(task)
        question5.add_question2task(task)


    def test_task_delete(self):
        self.unit.add()
        checkunit = db.session.query(Unit).filter(Unit.id == '1').one()
        checkunit.delete()
