# tests/test_models.py


import datetime
import unittest

from flask.ext.login import current_user

from project import bcrypt, db
from project.util import BaseTestCase
from project.models import User
from project.token import generate_confirmation_token, confirm_token


class TestUser(BaseTestCase):

    # def test_user_registration(self):
    #     # Ensure user registration behaves correctly.
    #     with self.client:
    #         self.client.post('/register', data=dict(
    #             email='test@user.com',
    #             password='test_user', confirm='test_user'
    #         ), follow_redirects=True)
    #         user = User.query.filter_by(email='test@user.com').first()
    #         self.assertTrue(user.id)
    #         self.assertTrue(user.email == 'test@user.com')
    #         self.assertFalse(user.admin)

    def test_get_by_id(self):
        # Ensure id is correct for the current/logged in user
        with self.client:
            self.client.post('/login', data=dict(
                email='ad@min.com', password='admin_user'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)

    def test_registered_on_defaults_to_datetime(self):
        # Ensure that registered_on is a datetime
        with self.client:
            self.client.post('/login', data=dict(
                email='ad@min.com', password='admin_user'
            ), follow_redirects=True)
            user = User.query.filter_by(email='ad@min.com').first()
            self.assertIsInstance(user.registered_on, datetime.datetime)

    def test_check_password(self):
        # Ensure given password is correct after unhashing
        user = User.query.filter_by(email='ad@min.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin_user'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

    def test_validate_invalid_password(self):
        # Ensure user can't login when the pasword is incorrect
        with self.client:
            response = self.client.post('/login', data=dict(
                email='ad@min.com', password='foo_bar'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email and/or password.', response.data)

    def test_invalid_confirmation_token(self):
        user1 = User(email='test@test1.com', password='test1', confirmed=False)
        user2 = User(email='test@test2.com', password='test2', confirmed=False)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = generate_confirmation_token('test@test2.com')
        confirm_token(token)
        self.assertFalse(user1.confirmed)

    def test_invalid_confirmation_token_views(self):
        user1 = User(email='test@test1.com', password='test1', confirmed=False)
        user2 = User(email='test@test2.com', password='test2', confirmed=False)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = generate_confirmation_token('test@test2.com')
        with self.client:
            self.client.post('/login', data=dict(
                email='test@test1.com', password='test1'
            ), follow_redirects=True)
            response = self.client.get(
                '/confirm/'+str(token), follow_redirects=True)
            self.assertIn('The confirmation link is invalid or has expired.',
                          response.data)


if __name__ == '__main__':
    unittest.main()
