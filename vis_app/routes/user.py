from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser
#from utils import validate_user
logging.basicConfig(level=logging.DEBUG)
from vis_app.Models.User import User

start_time = ""
end_time = ""

user = Blueprint('user', __name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')


"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
visitor_col = ['user_id', 'first_name', 'middle_name', 'last_name', 'contact_number', 'entry_time', 'people_count', 'society_id', 'flat_id',
               'visit_reason', 'visitor_status', 'whom_to_visit', 'vehicle', 'photo','otp']

verdict_visitor = {}

'''looping to check data type and prepare column value'''
for each_column in visitor_col:
    verdict_visitor[each_column] = None


@user.route('/get_society_members_details', methods=['GET', 'POST'])
def get_society_members_details():
    """get list of wings from a Society"""
    try:
        society_id = request.form['society_id']
        society_members_details = queries['get_society_members_details']
        query = society_members_details.format(society_id)

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)
        return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'get_wing_list': False, 'error': (error)}
        return str(errors)


@user.route('/user/register', methods=['GET','POST'])
def user_register():
    """Society Member Registration """
    # username=request.form['username']
    email = request.form['email']
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    password = request.form['password']
    society_id = request.form['society_id']
    flat_id = request.form['flat_id']
    isadmin = request.form['isadmin']
    user_status = request.form['user_status']
    username = request.form['email']

    df = pd.DataFrame({'username': str(username),
                       'email': str(email),
                       'first_name': str(first_name),
                       'middle_name': str(middle_name),
                       'last_name': str(last_name),
                       'password': str(password),
                       'society_id': str(society_id),
                       'isadmin': str(isadmin),
                       'flat_id': str(flat_id),
                       'user_entity': str(user_status)
                       },
                      index=[0])

    query = queries['get_user_id'].format(email)
    try:
        with dbm.dbManager() as manager:
            manager.commit(df, 'visitor_management_schema.user_table')
            user_id = manager.getDataFrame(query)
            return jsonify(user_id.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'registration': False, 'error': error}
        return str(errors)


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
    username = request.form['email']
    identification_type = request.form['identification_type']
    identification_no = request.form['identification_no']
    identification_no = request.form['identification_no']

    df = pd.DataFrame({'username': str(username),
                       'email': str(email),
                       'first_name': str(first_name),
                       'middle_name': str(middle_name),
                       'last_name': str(last_name),
                       'password': str(password),
                       'society_id': str(society_id),
                       'isadmin': str(isadmin),
                       'user_entity': str(user_status),
                       'identification_type': str(identification_type),
                       'identification_no': str(identification_no)
                       },
                      index=[0])

    try:

        with dbm.dbManager() as manager:
            manager.commit(df, 'visitor_management_schema.user_table')
        return "User registered Successfully"
    except psycopg2.DatabaseError as error:
        errors = {'registration': False, 'error': error}
        return str(errors)


@user.route('/user/login', methods=['GET', 'POST'])
def login():
    logging.info("Running Login")
    username = request.form['username']
    password = request.form['password']

    #validate_user(username, password)
    user = User.select().where(User.username == username)
    if user is not None:
        #check_password(username,password)
        u = user.get()
        if u.password == password:
                return User.serialize(user)
    else:
        return 'User does not exist'


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


@user.route('/update_user_photo', methods=['GET','POST'])
def update_user_photo():
    """
    update user photo
    requires user id
    """
    user_id = request.form['user_id']
    photo = request.form['photo']

    query = queries['update_user_photo'].format(photo, user_id)

    try:
        with dbm.dbManager() as manager:
            result = manager.updateDB(query)
        success = True
    except:
        success = False

    return jsonify(success)


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


@user.route('/user/set_user_login_status', methods=['GET', 'POST'])
def set_user_login_status():
    user_id = request.form['user_id']
    user_status = request.form['user_status']
    logging.info('Setting User id: %s status set to %s', user_id, user_status)
    query_approve_user = queries['set_user_login_status']

    set_approve_user_query = query_approve_user.format(user_status, user_id)
    logging.info('query generated %s', set_approve_user_query)
    with dbm.dbManager() as manager:
        result = manager.updateDB(set_approve_user_query)
        logging.info('User id: %s  login status set to %s', user_id, user_status)
        return jsonify(bool(result))


@user.route('/user/set_user_admin_status', methods=['GET', 'POST'])
def set_user_admin_status():
    user_id = request.form['user_id']
    user_admin_status = request.form['user_admin_status']
    logging.info('Setting User id: %s status set to %s', user_id, user_admin_status)
    query_update_user_admin = queries['set_user_admin_status']

    set_approve_user_query = query_update_user_admin.format(user_admin_status, user_id)
    with dbm.dbManager() as manager:
        result = manager.updateDB(set_approve_user_query)
        logging.info('User id: %s  admin status set to %s', user_id, user_admin_status)
        return jsonify(bool(result))
