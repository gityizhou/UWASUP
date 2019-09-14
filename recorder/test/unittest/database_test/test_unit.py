import unittest

from recorder import create_app, db
from recorder.models.unit import Unit


class TestUnit(unittest.TestCase):

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

    def test_unit_create(self):
        unit = Unit(unit_id="CITS1401",
                         unit_name="Python")
        unit.add()

    def test_unit_get_tasks(self):
        tasks = db.session.query(Unit).filter(Unit.id == '1').first().tasks
        print(tasks)


    def test_unit_delete(self):
        self.unit.add()
        checkunit = db.session.query(Unit).filter(Unit.id == '1').one()
        checkunit.delete()
