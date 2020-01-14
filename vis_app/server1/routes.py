from flask import Blueprint


s1 = Blueprint('s1', __name__)


@s1.route('/homepage')
def homepage():
    return 'you are on the home page'