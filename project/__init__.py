# project/__init__.py


#################
#### imports ####
#################

import os

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask_mail import Mail
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy


################
#### config ####
################

def _check_config_variables_are_set(config):
    assert config['MAIL_USERNAME'] is not None,\
           'MAIL_USERNAME is not set, set the env variable APP_MAIL_USERNAME '\
           'or MAIL_USERNAME in the production config file.'
    assert config['MAIL_PASSWORD'] is not None,\
           'MAIL_PASSWORD is not set, set the env variable APP_MAIL_PASSWORD '\
           'or MAIL_PASSWORD in the production config file.'

    assert config['SECRET_KEY'] is not None,\
           'SECRET_KEY is not set, set it in the production config file.'
    assert config['SECURITY_PASSWORD_SALT'] is not None,\
           'SECURITY_PASSWORD_SALT is not set, '\
           'set it in the production config file.'

    assert config['SQLALCHEMY_DATABASE_URI'] is not None,\
           'SQLALCHEMY_DATABASE_URI is not set, '\
           'set it in the production config file.'

    if os.environ['APP_SETTINGS'] == 'project.config.ProductionConfig':
        assert config['STRIPE_SECRET_KEY'] is not None,\
               'STRIPE_SECRET_KEY is not set, '\
               'set it in the production config file.'
        assert config['STRIPE_PUBLISHABLE_KEY'] is not None,\
               'STRIPE_PUBLISHABLE_KEY is not set, '\
               'set it in the production config file.'


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

_check_config_variables_are_set(app.config)

####################
#### extensions ####
####################

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)


####################
#### blueprints ####
####################

from project.main.views import main_blueprint
from project.user.views import user_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)


####################
#### flask-login ####
####################

from project.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


########################
#### error handlers ####
########################

@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
