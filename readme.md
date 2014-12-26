# Flask Registration

[![Build Status](https://travis-ci.org/realpython/flask-registration.svg?branch=master)](https://travis-ci.org/realpython/flask-registration)

Starter app for managing users - login/logout, registration, and email confirmation.

## QuickStart

### Set Environment Variables

```sh
$ export APP_SETTINGS="project.config.DevelopmentConfig"
$ export APP_MAIL_USERNAME="foo"
$ export APP_MAIL_PASSWORD="bar"
```

or

```sh
$ export APP_SETTINGS="project.config.ProductionConfig"
$ export APP_MAIL_USERNAME="foo"
$ export APP_MAIL_PASSWORD="bar"
```

### Update Settings in Production

1. `SECRET_KEY`
1. `SQLALCHEMY_DATABASE_URI`

### Create DB

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
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
