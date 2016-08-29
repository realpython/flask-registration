How to contribute
-----------------

## env.sh

You can create a file `env.sh` with the settings needed to setup the needed development (or testing) environment variables.

```sh
#!/usr/bin/env bash

function app_clean_env() {
    unset APP_MAIL_SERVER
    unset APP_MAIL_PORT
    unset APP_MAIL_USE_TLS
    unset APP_MAIL_USE_SSL
    unset APP_MAIL_USERNAME
    unset APP_MAIL_PASSWORD
    unset APP_MAIL_DEFAULT_SENDER
    unset APP_SQLALCHEMY_DATABASE_URI
}

app_clean_env

if [[ "$APP_SETTINGS" == 'project.config.DevelopmentConfig' ]]; then
    echo "Apply DevelopmentConfig settings"

    # mail setting
    export APP_MAIL_SERVER='<your_smtp_server>'
    export APP_MAIL_PORT='<your_smtp_server_port>'
    export APP_MAIL_USE_TLS='<true_or_false>'
    export APP_MAIL_USE_SSL='<true_or_false>'

    # mail authentication
    export APP_MAIL_USERNAME='<your_smtp_username>'
    export APP_MAIL_PASSWORD='<your_smtp_password>'

elif [[ "$APP_SETTINGS" == 'project.config.TestingConfig' ]]; then
    echo "Apply TestingConfig settings"
    # put your testing settings here

elif [[ "$APP_SETTINGS" == 'project.config.ProductionConfig' ]]; then
    echo "Apply ProductionConfig settings"
    # put your production settings here

else
    (>&2 echo "Unrecognized setting")
fi
```

## Sending and debugging emails

To send email for development, testing and production you can use your own hosted SMTP server or other solutions. Here's two examples:

* [Mailgun](https://mailgun.com)
You can use Mailgun if you want to send emails in production.

* [Debug Mail](https://mailgun.com)
Debug Mail is a tool to debut email, you can use it for developing testing.

Both services offer free plans that you can use for developing and testing `flask-registration`.

## Develop locally

You can use the scripts `clean.sh` and `create.sh` to setup the environment.

You need to set up the `APP_SETTINGS` variable:

```sh
export APP_SETTINGS=project.config.DevelopmentConfig
```

To run the development server:
```bash
./clean.sh; source env.sh && ./create.sh && python manage.py runserver
```

To run the tests:
```bash
./clean.sh; source env.sh && python manage.py test
```

## Use Travis to run tests

1. Fork the repository
2. if you don't have an account on [Travis](http://travis-ci.org/), create it (it's free)
3. Add your `flask-registration` repository on the Travis settings page.
4. In Travis, click of the cog icon next to the repository and add the following [environment variables](https://docs.travis-ci.com/user/environment-variables/#Defining-Variables-in-Repository-Settings):

```
APP_SETTINGS: project.config.TestingConfig
APP_MAIL_SERVER: <your_smtp_server>
APP_MAIL_PORT: <your_smtp_server_port>
APP_MAIL_USERNAME: <your_smpt_username>
APP_MAIL_PASSWORD: <your_smpt_password>
```

You can use any valid SMTP credentials, the defaults are the following:

```
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
```

When you commit to your repository, travis will automatically build the application with the testing settings (see the file `.travis.yml`.
