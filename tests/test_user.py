import datetime
import unittest

from flask_login import current_user

from project import db
from project.models import User
from project.util import BaseTestCase
from project.user.forms import RegisterForm, \
    LoginForm, ChangePasswordForm, ForgotForm
from project.token import generate_confirmation_token, confirm_token


class TestUserForms(BaseTestCase):

    def test_validate_success_register_form(self):
        # Ensure correct data validates.
        form = RegisterForm(
            email='new@test.test',
            password='example', confirm='example')
        self.assertTrue(form.validate())

    def test_validate_invalid_password_format(self):
        # Ensure incorrect data does not validate.
        form = RegisterForm(
            email='new@test.test',
            password='example', confirm='')
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        # Ensure user can't register when a duplicate email is used
        form = RegisterForm(
            email='test@user.com',
            password='just_a_test_user',
            confirm='just_a_test_user'
        )
        self.assertFalse(form.validate())

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='test@user.com', password='just_a_test_user')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())

    def test_validate_success_change_password_form(self):
        # Ensure correct data validates.
        form = ChangePasswordForm(password='update', confirm='update')
        self.assertTrue(form.validate())

    def test_validate_invalid_change_password(self):
        # Ensure passwords must match.
        form = ChangePasswordForm(password='update', confirm='unknown')
        self.assertFalse(form.validate())

    def test_validate_invalid_change_password_format(self):
        # Ensure invalid email format throws error.
        form = ChangePasswordForm(password='123', confirm='123')
        self.assertFalse(form.validate())

    def test_validate_success_forgot_password(self):
        # Ensure invalid email format throws error.
        form = ForgotForm(email='test@user.com')
        self.assertTrue(form.validate())

    def test_validate_invalid_forgot_password_format(self):
        # Ensure invalid email format throws error.
        form = ForgotForm(email='unknown')
        self.assertFalse(form.validate())

    def test_validate_invalid_forgot_password_no_such_user(self):
        # Ensure invalid email format throws error.
        form = ForgotForm(email='not@correct.com')
        self.assertFalse(form.validate())


class TestUserViews(BaseTestCase):

    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="test@user.com", password="just_a_test_user"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertTrue(current_user.email == "test@user.com")
            self.assertTrue(current_user.is_active())
            self.assertTrue(current_user.is_authenticated())
            self.assertTemplateUsed('main/index.html')

    def test_incorrect_login(self):
        # Ensure login behaves correctly with incorrect credentials.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="not@correct.com", password="incorrect"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertIn(b'Invalid email and/or password.', response.data)
            self.assertFalse(current_user.is_active())
            self.assertFalse(current_user.is_authenticated())
            self.assertTemplateUsed('user/login.html')

    def test_profile_route_requires_login(self):
        # Ensure profile route requires logged in user.
        self.client.get('/profile', follow_redirects=True)
        self.assertTemplateUsed('user/login.html')

    def test_confirm_token_route_requires_login(self):
        # Ensure confirm/<token> route requires logged in user.
        self.client.get('/confirm/blah', follow_redirects=True)
        self.assertTemplateUsed('user/login.html')

    def test_confirm_token_route_valid_token(self):
        # Ensure user can confirm account with valid token.
        with self.client:
            self.client.post('/login', data=dict(
                email='test@user.com', password='just_a_test_user'
            ), follow_redirects=True)
            token = generate_confirmation_token('test@user.com')
            response = self.client.get(
                '/confirm/'+token, follow_redirects=True)
            self.assertIn(
                b'You have confirmed your account. Thanks!', response.data)
            self.assertTemplateUsed('main/index.html')
            user = User.query.filter_by(email='test@user.com').first_or_404()
            self.assertIsInstance(user.confirmed_on, datetime.datetime)
            self.assertTrue(user.confirmed)

    def test_confirm_token_route_invalid_token(self):
        # Ensure user cannot confirm account with invalid token.
        token = generate_confirmation_token('test@test1.com')
        with self.client:
            self.client.post('/login', data=dict(
                email='test@user.com', password='just_a_test_user'
            ), follow_redirects=True)
            response = self.client.get('/confirm/'+token,
                                       follow_redirects=True)
            self.assertIn(
                b'The confirmation link is invalid or has expired.',
                response.data
            )

    def test_confirm_token_route_expired_token(self):
        # Ensure user cannot confirm account with expired token.
        user = User(email='test@test1.com', password='test1', confirmed=False)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token('test@test1.com')
        self.assertFalse(confirm_token(token, -1))

    def test_forgot_password_does_not_require_login(self):
        # Ensure user can request new password without login.
        self.client.get('/forgot', follow_redirects=True)
        self.assertTemplateUsed('user/forgot.html')

    def test_correct_forgot_password_request(self):
        # Ensure login behaves correctly with correct credentials.
        with self.client:
            response = self.client.post(
                '/forgot',
                data=dict(email="test@user.com"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertTemplateUsed('main/index.html')

    def test_reset_forgotten_password_valid_token(self):
        # Ensure user can confirm account with valid token.
        with self.client:
            self.client.post('/forgot', data=dict(
                email='test@user.com',
            ), follow_redirects=True)
            token = generate_confirmation_token('test@user.com')
            response = self.client.get('/forgot/new/'+token, follow_redirects=True)
            self.assertTemplateUsed('user/forgot_new.html')
            self.assertIn(
                b'You can now change your password.',
                response.data
            )
            self.assertFalse(current_user.is_authenticated())

    def test_reset_forgotten_password_valid_token_correct_login(self):
        # Ensure user can confirm account with valid token.
        with self.client:
            self.client.post('/forgot', data=dict(
                email='test@user.com',
            ), follow_redirects=True)
            token = generate_confirmation_token('test@user.com')
            response = self.client.get('/forgot/new/'+token, follow_redirects=True)
            self.assertTemplateUsed('user/forgot_new.html')
            self.assertIn(
                b'You can now change your password.',
                response.data
            )
            response = self.client.post(
                '/forgot/new/'+token,
                data=dict(password="new-password", confirm="new-password"),
                follow_redirects=True
            )
            self.assertIn(
                b'Password successfully changed.',
                response.data
            )
            self.assertTemplateUsed('user/profile.html')
            self.assertTrue(current_user.is_authenticated())
            self.client.get('/logout')
            self.assertFalse(current_user.is_authenticated())

            response = self.client.post(
                '/login',
                data=dict(email="test@user.com", password="new-password"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertTrue(current_user.email == "test@user.com")
            self.assertTrue(current_user.is_active())
            self.assertTrue(current_user.is_authenticated())
            self.assertTemplateUsed('main/index.html')

    def test_reset_forgotten_password_valid_token_invalid_login(self):
        # Ensure user can confirm account with valid token.
        with self.client:
            self.client.post('/forgot', data=dict(
                email='test@user.com',
            ), follow_redirects=True)
            token = generate_confirmation_token('test@user.com')
            response = self.client.get('/forgot/new/'+token, follow_redirects=True)
            self.assertTemplateUsed('user/forgot_new.html')
            self.assertIn(
                b'You can now change your password.',
                response.data
            )
            response = self.client.post(
                '/forgot/new/'+token,
                data=dict(password="new-password", confirm="new-password"),
                follow_redirects=True
            )
            self.assertIn(
                b'Password successfully changed.',
                response.data
            )
            self.assertTemplateUsed('user/profile.html')
            self.assertTrue(current_user.is_authenticated())
            self.client.get('/logout')
            self.assertFalse(current_user.is_authenticated())

            response = self.client.post(
                '/login',
                data=dict(email="test@user.com", password="just_a_test_user"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertFalse(current_user.is_authenticated())
            self.assertIn(
                b'Invalid email and/or password.',
                response.data
            )
            self.assertTemplateUsed('user/login.html')


if __name__ == '__main__':
    unittest.main()
