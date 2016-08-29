# project/main/views.py


#################
#### imports ####
#################

from flask import render_template
from flask import Blueprint
from flask_login import current_user
from flask_login import login_required

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/')
def home():
    return render_template('main/index.html', current_user=current_user)
