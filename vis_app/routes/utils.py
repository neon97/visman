from vis_app.Models.User import User
from flask import Response
import pandas as pd

def query_to_json(query):
    if query.count() == 0 :
            return "No results found"
    else:
        df = pd.DataFrame.from_dict(query) 
        result = df.to_json(orient='records')
        return Response(result,mimetype='application/json')


def validate_user(username, password):
    user = User.select().where(User.username == username)
    if user is not None:
        check_password(username,password)
        if user.password == password:
                return User.serialize(user)
    else:
        return 'User does not exist'

def check_password(username, password):
    pass




def replace(data):
    if data is not None:
        return data
    data = None
    return data


def generate(first,last):
    return first+last


def generate_otp(user_id, visitor_id):
    OTP = random.randint(1000, 9999);
    created = datetime.now();
    df = pd.DataFrame({'OTP': OTP, 'created': created, 'user_id': user_id,
                       'visitor_id': visitor_id}, index=[0])
    with dbm.dbManager() as manager:
        manager.commit(df, 'visitor_management_schema.opt')
        return OTP;

