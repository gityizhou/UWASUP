import unittest

from recorder import create_app, db
from recorder.models.unit import Unit
from recorder.models.task import Task
from recorder.models.user import User
from recorder.models.user_task import User_task
from pandas import DataFrame
import os


class TestTask(unittest.TestCase):

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

    # create task
    def test_task_create(self):
        task = Task(task_name="Write 5 Essays", description="please write 5 essays, similarity under 8.8%")
        task.add()

    # add tasks to unit
    def test_addtask2unit(self):
        unit = db.session.query(Unit).filter(Unit.id == '1').one()
        task = db.session.query(Task).filter(Task.id == '1').one()
        task.add_task2unit(unit)

    # query questions under a task
    def test_query_questions(self):
        questions = db.session.query(Task).filter(Task.id == '1').one().questions
        print(questions)

    # update a task
    def test_task_update(self):
        task = db.session.query(Task).filter(Task.id == '1').one()
        task.task_name = "something test"
        task.update()

    # !!!!!delete a task
    def test_task_delete(self):
        task = db.session.query(Task).filter(Task.id == '2').one()
        task.delete()

    def test_task_users(self):
        task = db.session.query(Task).filter(Task.id == '1').one()
        users = task.get_task_users()
        for user in users:
            print(type(user))
            print(user.email)


    def test_get_user_task(self):
        User_task.get_user_task(1, 1)

    def test_get_tasks(self):
        results = User_task.query.filter_by(task_id=1)
        this_task = db.session.query(Task).filter(Task.id == 1).one()
        dir = os.getcwd() + "/csv/" + this_task.task_name + "_" + str(this_task.id) + ".csv"
        filename = "./csv/" + this_task.task_name + "_" + str(this_task.id) + ".csv"
        student_number = []
        first_name = []
        last_name = []
        mark = []
        for i in results:
            id = i.user_id
            student = db.session.query(User).filter(User.id == id).one()
            mark.append(i.mark)
            first_name.append(student.first_name)
            last_name.append(student.last_name)
            student_number.append(student.user_number)
        data = {'student_number': student_number,
                'first_name': first_name,
                'last_name': last_name,
                'mark': mark}
        df = DataFrame(data)
        columns = ['student_number', 'first_name', 'last_name', 'mark']
        print(os.getcwd())
        df.to_csv(dir, encoding="utf_8_sig", index=False, columns=columns)
        print(df)

        # print(student_number)
        # print(first_name)
        # print(last_name)
        # print(mark)

    def test_delete_csv(self):
        Task.delete_csv(1)
