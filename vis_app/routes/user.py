from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser
from peewee import IntegrityError, DoesNotExist
#from utils import validate_user
logging.basicConfig(level=logging.DEBUG)
from vis_app.Models.User import User
from flask_bcrypt import Bcrypt
from vis_app.Models.BaseModel import db

import json
start_time = ""
end_time = ""

user = Blueprint('user', __name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')

bcrypt = Bcrypt()

"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
user_col = ['email', 'first_name', 'middle_name', 'last_name','password', 'contact_number', 'society_id', 
            'flat_id','isadmin','user_entity','photo']

# verdict_user = {}

# '''looping to check data type and prepare column value'''
# for each_column in user_col:
#     verdict_user[each_column] = None


@user.route('/get_society_members_details', methods=['GET', 'POST'])
def get_society_members_details():
    """get list of wings from a Society"""
    try:
        society_id = request.form['society_id']
        society_members_details = queries['get_society_members_details']
        query = society_members_details.userformat(society_id)

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)
        return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'get_wing_list': False, 'error': (error)}
        return str(errors)


@user.route('/user/register', methods=['GET','POST'])
def user_register():
    """Society Member Registration """

    email = request.form['email']
    username = email
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    password = request.form['password']
    society_id = request.form['society_id']
    flat_id = request.form['flat_id']
    isadmin = request.form['isadmin']
    user_entity = request.form['user_status']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User()

    user.username = email
    user.email = email
    user.first_name = first_name
    user.middle_name = middle_name
    user.last_name= last_name
    user.password = hashed_password
    user.society_id = society_id
    user.flat_id = flat_id
    user.isadmin = isadmin
    user.user_entity = user_entity

    try :
        user.save()
        return 'User created successfully'

    except psycopg2.errors.UniqueViolation as e:
            return 'User already exists.'          
        
    except Exception as e:
        errors = {'User registration Failed , error is : ': e}
        return str(errors)



    # user = User()
    # for each_col in user_col:
    #     #logging.info("key is : %s", each_col)
    #     try:
    #         #logging.info("value is %s", request.form[each_col])
    #         user.each_col = request.form[each_col]
    #         logging.info("key %s, value is %s", each_col,user.each_col)
    #     except:
    #         user.each_col = None

    #     finally:
    #         logging.info("in finally")
    #         logging.info("key %s, value is %s", each_col,user.each_col)
            
    
    #user.username = request.form['email']
    #for att in user_col:
    




@user.route('/user/register/staff', methods=['GET', 'POST'])
def user_register_staff():
    """staff Registration (staff may be like watchman or society accounts guy)
    """
    email = request.form['email']
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    password = request.form['password']
    society_id = request.form['society_id']
    isadmin = request.form['isadmin']
    user_status = request.form['user_status']
    identification_type = request.form['identification_type']
    identification_no = request.form['identification_no']
    identification_no = request.form['identification_no']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User()

    user.username = email
    user.email = email
    user.first_name = first_name
    user.middle_name = middle_name
    user.last_name= last_name
    user.password = hashed_password
    user.society_id = society_id
    user.isadmin = isadmin
    user.user_entity = user_status
    user.identification_type = identification_type
    user.identification_no = identification_no
                             

    try :
        user.save()
        return 'User created successfully'

    except psycopg2.errors.UniqueViolation as e:
            return 'User not already exists.'          
        
    except Exception as e:
        errors = {'User registration Failed , error is : ': e}
        return str(errors)

@user.route('/user/login', methods=['GET', 'POST'])
def login():
    logging.info("Running Login")
    username = request.form['username']
    password = request.form['password']

    try:
        user = User.get(User.username == username)
        logging.info('user is %s', user.username)
            #return 'Login successfull'
        if bcrypt.check_password_hash(user.password, password):
            #user.password == password:

             return 'Login successfull'
        else:
            return 'Login failed: Password does not mach'
    
    except User.DoesNotExist:
        return 'User does not exist'

    except Exception as error :
        errors = {'error': error}
        return str(errors)
    


@user.route('/get_login_details', methods=['GET', 'POST'])
def get_login_details():
    """
        get the details of user by the user id.
    """
    user_id = request.form['user_id']
    query = queries['user_login_details']
    user_details_query = query.format(user_id)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(user_details_query)
        return jsonify(result.to_dict(orient='records'))





#admin access
@user.route('/dashboard_staff', methods=['GET', 'POST'])
def dashboard_staff():
    society_id = request.form['society_id']
    query_society_staff = queries['society_staff_list']

    query = query_society_staff.format(society_id)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query)

    return jsonify(result.to_dict(orient='records'))


@user.route('/dashboard_members', methods=['GET', 'POST'])
def dashboard_members():
    society_id = request.form['society_id']
    user_status = request.form['user_status']
    query_society_staff = queries['society_members_list']

    query = query_society_staff.format(user_status, society_id)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query)

    return jsonify(result.to_dict(orient='records'))



@user.route('/user/set/photo', methods=['GET','POST'])
@user.route('/update_user_photo', methods=['GET','POST'])
def update_user_photo():
    """
    update user photo
    requires user id
    """
    user_id = request.form['user_id']
    photo = request.form['photo']

    try:
        user = User.get(User.id == user_id)
        user.photo = photo
        use.save()
        success = True
    except Exception as error:
        logging.debug(error)
        success = False

    return jsonify(success)


@user.route('/user/set/ogin_status', methods=['GET', 'POST'])
@user.route('/user/set_user_login_status', methods=['GET', 'POST'])
def set_user_login_status():
    user_id = request.form['user_id']
    user_entity = request.form['user_status']
    logging.info('Setting User id: %s status set to %s', user_id, user_entity)
    try:
        user = User.get(User.id == user_id)
        user.user_entity = user_entity
        use.save()
        success = True
    except Exception as error:
        logging.debug(error)
        success = False

    return jsonify(success)


@user.route('/user/set/admin_status', methods=['GET', 'POST'])
@user.route('/user/set_user_admin_status', methods=['GET', 'POST'])
def set_user_admin_status():
    user_id = request.form['user_id']
    user_admin_status = request.form['user_admin_status']
    logging.info('Setting User id: %s status set to %s', user_id, user_admin_status)
    try:
        user = User.get(User.id == user_id)
        user.isadmin = user_admin_status
        use.save()
        success = True
    except Exception as error:
        logging.debug(error)
        success = False

    return jsonify(success)