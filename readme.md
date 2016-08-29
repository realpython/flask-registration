# Flask Registration

[![Build Status](https://travis-ci.org/realpython/flask-registration.svg?branch=master)](https://travis-ci.org/realpython/flask-registration)

Starter app for managing users - login/logout, registration, and email confirmation.

**Blog posts:**

- Part 1: [Handling Email Confirmation During Registration in Flask](https://realpython.com/blog/python/handling-email-confirmation-in-flask)
- Part 2: [The Minimum Viable Test Suite](https://realpython.com/blog/python/the-minimum-viable-test-suite/)

## QuickStart

### Set Environment Variables

Development Example (with [Debug Mail](https://debugmail.io)):

```sh
$ export APP_SETTINGS="project.config.DevelopmentConfig"
$ export APP_MAIL_SERVER=debugmail.io
$ export APP_MAIL_PORT=25
$ export APP_MAIL_USE_TLS=true
$ export APP_MAIL_USE_SSL=false
$ export APP_MAIL_USERNAME=ADDYOUROWN
$ export APP_MAIL_PASSWORD=ADDYOUROWN
```

Production Example:

```sh
$ export APP_SETTINGS="project.config.ProductionConfig"
$ export APP_MAIL_SERVER=ADDYOUROWN
$ export APP_MAIL_PORT=ADDYOUROWN
$ export APP_MAIL_USE_TLS=ADDYOUROWN
$ export APP_MAIL_USE_SSL=ADDYOUROWN
$ export APP_MAIL_USERNAME=ADDYOUROWN
$ export APP_MAIL_PASSWORD=ADDYOUROWN
```

### Update Settings in Production

1. `SECRET_KEY`
1. `SQLALCHEMY_DATABASE_URI`

### Create DB

Run:

```sh
$ sh create.sh
```

Or:

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
```

Want to clean the environment? Run:

```sh
sh clean.sh
```

### Run

```sh
$ python manage.py runserver
```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```
