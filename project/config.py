# project/config.py

import os
try:
    # Python 2.7
    import ConfigParser as configparser
except ImportError:
    # Python 3
    import configparser

basedir = os.path.abspath(os.path.dirname(__file__))


def _get_bool_env_var(varname, default=None):

    value = os.environ.get(varname, default)

    if value is None:
        return False
    elif isinstance(value, str) and value.lower() == 'false':
        return False
    elif bool(value) is False:
        return False
    else:
        return bool(value)


class BaseConfig(object):
    """Base configuration."""

    # main config
    SECRET_KEY = 'my_precious'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    # defaults are:
    #  - MAIL_SERVER = 'smtp.googlemail.com'
    #  - MAIL_PORT = 465
    #  - MAIL_USE_TLS = False
    #  - MAIL_USE_SSL = True
    MAIL_SERVER = os.environ.get('APP_MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('APP_MAIL_PORT', 465))
    MAIL_USE_TLS = _get_bool_env_var('APP_MAIL_USE_TLS', False)
    MAIL_USE_SSL = _get_bool_env_var('APP_MAIL_USE_SSL', True)

    # mail authentication
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD', None)

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    LOGIN_DISABLED=False
    TESTING = True
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    DEBUG_TB_ENABLED = False

    SECRET_KEY = None
    SECURITY_PASSWORD_SALT = None

    STRIPE_SECRET_KEY = None
    STRIPE_PUBLISHABLE_KEY = None

    SQLALCHEMY_DATABASE_URI = None

    # production config takes precedence over env variables

    # production config file at ./project/config/production.cfg
    config_path = os.path.join(basedir, 'config', 'production.cfg')

    # if config file exists, read it:
    if os.path.isfile(config_path):
        config = configparser.ConfigParser()

        with open(config_path) as configfile:
            config.readfp(configfile)

        SECRET_KEY = config.get('keys', 'SECRET_KEY')
        SECURITY_PASSWORD_SALT = config.get('keys', 'SECRET_KEY')

        # mail settings
        MAIL_SERVER = config.get('mail', 'MAIL_SERVER')
        MAIL_PORT = config.getint('mail', 'MAIL_PORT')
        MAIL_USE_TLS = config.getboolean('mail', 'MAIL_USE_TLS')
        MAIL_USE_SSL = config.getboolean('mail', 'MAIL_USE_SSL')

        # mail authentication and sender
        MAIL_USERNAME = config.get('mail', 'MAIL_USERNAME')
        MAIL_PASSWORD = config.get('mail', 'MAIL_PASSWORD')
        MAIL_DEFAULT_SENDER = config.get('mail', 'MAIL_DEFAULT_SENDER')

        # database URI
        SQLALCHEMY_DATABASE_URI = config.get('db', 'SQLALCHEMY_DATABASE_URI')

        # stripe keys
        STRIPE_SECRET_KEY = config.get('stripe', 'STRIPE_SECRET_KEY')
        STRIPE_PUBLISHABLE_KEY = config.get('stripe', 'STRIPE_PUBLISHABLE_KEY')
