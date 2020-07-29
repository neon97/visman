from vis_app.Models.User import User
from flask import Response, jsonify, session, g
import pandas as pd
from vis_app.Models.BaseModel import BaseModel
import logging
from vis_app.Models import User
import json
from playhouse.shortcuts import model_to_dict


class CustResponse:

    def send(message, status, outParams):
        logging.debug("In function send")
        print(status, message, outParams)
        response = {"Message": message, "Status": status, "Result": outParams}
        return response


def query_to_json(query):
    logging.debug("In function query_to_json")
    logging.debug("Running query : {}".format(query))
    try:
        if query.count() == 0:
            return CustResponse.send("No Records Found", False, None)
        else:
            # result = [dict(model_to_dict(c)) for c in query]
            df = pd.DataFrame.from_dict(query.dicts())
            result = json.loads(df.to_json(orient='records'))
            logging.info("returining result : %s", result)
            logging.debug("Returning result : {}".format(result))
            return CustResponse.send(" Successful", True, result)

    except Exception as error:
        logging.info("Query Failed with error {}".format(error))
        return CustResponse.send("UnSuccessful", False, str(error))


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


def response(func, message):
    status = func.status  # true or false
    msg = message
    response = func.response
    j_responce = make_to_json(response)
    jsn = {
        "ststus": status,
        "message": msg,
        "response": j_responce
    }
