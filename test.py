from flask import request, jsonify, Flask
import json

from model.routes import *

#if __name__ == '__main__':

    #s = user.User.get_society_by_email('pandey')
    #print(s)
    #
    # user_pandey = User.get_object_or_404(User, id='2')
    # print(user_pandey.password)

app = Flask(__name__)
#app.run()