import unittest

from recorder import create_app, db
from recorder.models.unit import Unit
from recorder.models.task import Task


class TestTask(unittest.TestCase):

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

    def test_task_create(self):
        task = Task(task_name="Write 5 Essays",description="please write 5 essays, similarity under 8.8%")
        task.add()

    def test_addtask2unit(self):

        unit = db.session.query(Unit).filter(Unit.id == '1').one()
        task = db.session.query(Task).filter(Task.id == '1').one()
        task.add_task2unit(unit)

    def test_query_questions(self):

        questions = db.session.query(Task).filter(Task.id == '1').one().questions
        print(questions)


    def test_task_delete(self):
        self.unit.add()
        checkunit = db.session.query(Unit).filter(Unit.id == '1').one()
        checkunit.delete()
