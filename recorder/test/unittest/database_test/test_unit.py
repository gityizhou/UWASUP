import unittest

from recorder import create_app, db
from recorder.models.unit import Unit


class TestUnit(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.unit = Unit(unit_id="CITS1401",
                         unit_name="Python",
                         teacher_id="22302319")
        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_unit_create(self):
        self.unit.add()
        checkunit = db.session.query(Unit).filter(Unit.id == '1').one()
        self.assertEqual(checkunit, self.unit)

    def test_unit_update(self):
        self.unit.add()
        checkunit = db.session.query(Unit).filter(Unit.id == '1').one()
        checkunit.unit_name = "Java"
        checkunit.update()
        self.assertEqual(checkunit.unit_name, "Java")

    def test_unit_delete(self):
        self.unit.add()
        checkunit = db.session.query(Unit).filter(Unit.id == '1').one()
        checkunit.delete()
