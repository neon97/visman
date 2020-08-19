from vis_app.Models.User import User
from flask import Response, jsonify, session, g
import pandas as pd
from vis_app.Models.BaseModel import BaseModel
import logging
from vis_app.Models import User
import json
from playhouse.shortcuts import model_to_dict



def CustResponseSend(message, status, outParams):
    logging.debug("In function send")
    print(status, message, outParams)
    response = {"Message": message, "Status": status, "Result": outParams}
    return response


def result_to_json(result):
    logging.debug("In function result_to_json")
    try:
        if result.count() == 0:
            return CustResponseSend("No Records Found", False, [])
        else:
            # result = [dict(model_to_dict(c)) for c in query]
            df = pd.DataFrame.from_dict(result.dicts())
            result = json.loads(df.to_json(orient='records'))
            logging.info("Fetched result : %s", result)
            logging.debug("Fetched result : {}".format(result))
            return CustResponseSend(" Successful", True, result)

    except Exception as error:
        logging.info("result_to_json():{} while fetching result".format(error))
        return CustResponseSend("Error : {}".format(str(error)), False, [])


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
