# tests/test_forms.py


import unittest

from project.util import BaseTestCase
from project.user.forms import RegisterForm, LoginForm


class TestRegisterForm(BaseTestCase):

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
            email='ad@min.com',
            password='admin_user',
            confirm='admin_user'
        )
        self.assertFalse(form.validate())


class TestLoginForm(BaseTestCase):

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='ad@min.com', password='admin_user')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()
