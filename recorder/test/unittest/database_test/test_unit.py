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
        # will delete all data after each test
        # with self.app.app_context():
        #     db.session.remove()
        #     db.drop_all()
        pass

    # create a unit
    def test_unit_create(self):
        unit = Unit(unit_id="CITS1401",
                    unit_name="Python")
        unit.add()

    # query tasks in this unit
    def test_unit_get_tasks(self):
        tasks = db.session.query(Unit).filter(Unit.id == '1').first().tasks
        print(tasks)

    def test_query_all_units(self):
        units = Unit.query.all()
        print(units)

    # update the unit
    def test_unit_update(self):
        unit = db.session.query(Unit).filter(Unit.id == '1').one()
        unit.unit_name = "someunit4test"
        unit.update()

    # !!!!delete the unit
    def test_unit_delete(self):
        unit = db.session.query(Unit).filter(Unit.id == '5').one()
        unit.delete()


