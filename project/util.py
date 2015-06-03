# project/util.py


from flask.ext.testing import TestCase

from project import app, db
from project.models import User


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    @classmethod
    def setUpClass(self):
        db.create_all()
        user = User(
            email="test@user.com",
            password="just_a_test_user",
            confirmed=False
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()
