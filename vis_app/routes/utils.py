from vis_app.Models.User import User
from flask import Response, jsonify, session, g
import pandas as pd
from vis_app.Models.BaseModel import BaseModel
import logging
from vis_app.Models import User


def query_to_json(query):

    if query.count() == 0:
        return "No results found"
    else:
        df = pd.DataFrame.from_dict(query.dicts())
        result = df.to_json(orient='records')
        logging.info("returining result : %s", result)
        return Response(result, mimetype='application/json')


def query_to_json1(query):

    list = []
    for data in query:
        list.append(BaseModel.serialize(data))
    return jsonify(list)


def replace(data):
    if data is not None:
        return data
    data = None
    return data


def generate(first, last):
    return first+last


# def generate_otp(user_id, visitor_id):
#     OTP = random.randint(1000, 9999);
#     created = datetime.now();
#     df = pd.DataFrame({'OTP': OTP, 'created': created, 'user_id': user_id,
#                        'visitor_id': visitor_id}, index=[0])
#     with dbm.dbManager() as manager:
#         manager.commit(df, 'visitor_management_schema.opt')
#         return OTP;

def auth_user(user):
    session['logged_in'] = True
    session['user'] = user.first_name
    session['username'] = user.username
    logging.info('You are logged in as %s' % (user.username))
