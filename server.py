#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 16:18:42 2019
@author: akshay72

Main file running the application.
"""
import psycopg2, config_parser
from flask import Flask, request, jsonify
import pandas as pd
import db_config.dbManager as dbm
import logging
import random

logging.basicConfig(level=logging.DEBUG)

from datetime import datetime

start_time = ""
end_time = ""

app = Flask(__name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')


"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
visitor_col = ['user_id', 'first_name', 'middle_name', 'last_name', 'contact_number', 'entry_time', 'people_count', 'society_id', 'flat_id',
               'visit_reason', 'visitor_status', 'whom_to_visit', 'vehicle', 'photo']

verdict_visitor = {}

'''looping to check data type and prepare column value'''
for each_column in visitor_col:
    verdict_visitor[each_column] = None



def replace(data):
    if data is not None:
        return data
    data = None
    return data


def generate(first,last):
    return first+last

def generate_otp(user_id, visitor_id):
    OTP = random.randint(0, 9999);
    created = datetime.now();
    df = pd.DataFrame({'OTP': OTP, 'created': created, 'user_id': user_id,
                       'visitor_id': visitor_id}, index=[0])
    with dbm.dbManager() as manager:
        manager.commit(db, 'visitor_management_schema.opt')
        return OTP;


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return "<div><b>Sorry!!<br/>Only team has access to database<b><a href='/about'>About</a></div>"


@app.route('/about', methods=['GET', 'POST'])
def about():
    return jsonify({'Company': 'Visitor Management',
                    'Dev center': 'Team Foundation',
                    'version': 'heroku test development'})


@app.route('/society_info', methods=['GET', 'POST'])
def society_info():
    """ Gives the society id and society name for all registered society."""
    try:
        query = queries['society_info']

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)
            logging.info(result)
            logging.info(result.to_dict(orient='records'))
        return jsonify(result.to_dict(orient='records'))

    except psycopg2.DatabaseError as error:
        errors = {'society info': False, 'error': error}
        return str(errors)


@app.route('/society_register', methods=['GET', 'POST'])
def society_register():
    """Register society"""
    try:
        # society details
        regd_no = request.form['regd_no']
        society_name = request.form['society_name']
        society_address = request.form['society_address']
        total_buildings = request.form['total_buildings']
        total_flats = request.form['total_flats']


        df = pd.DataFrame({'regd_no': regd_no, 'society_name': society_name, 'society_address': society_address,
                           'total_buildings': total_buildings, 'total_flats': total_flats}, index=[0])

        logging.info('Dataframe for New Society %s', df)
        with dbm.dbManager() as manager:
            manager.commit(df, 'visitor_management_schema.society_table')
            logging.info('Society registered successfully')
            return "Society registered successfully"

    except psycopg2.DatabaseError as error:
        errors = {'society registeration': False,
                  'error': (error)
                  }
        return str(errors)


@app.route('/get_society_id', methods=['GET', 'POST'])
def get_society_id():
    """ get the society id by passing the society registration."""
    try:
        regd_no = request.form['regd_no']
        query_society_id = queries['get_society_id']
        query = query_society_id.format(regd_no)
        
        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)

        return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'registeration': False, 'error': (error) }
        return str(errors)


@app.route('/get_wing_list', methods=['GET', 'POST'])
def get_wing_list():
    """get list of wings from a Society"""
    try:
        society_id = request.form['society_id']
        society_wing_list = queries['get_wing_list']
        query = society_wing_list.format(society_id)

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)
        return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'get_wing_list': False, 'error': (error)}
        return str(errors)


@app.route('/get_society_members_details', methods=['GET', 'POST'])
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


@app.route('/get_flat_list', methods=['GET', 'POST'])
def get_flat_list():
    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']
        wing_flats_list = queries['get_flat_list']
        query = wing_flats_list.format(society_id, wing_name)

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)

        return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'get_flat_list': False, 'error': (error)}
        return str(errors)


@app.route('/add_flat', methods=['GET', 'POST'])
def add_flat():
    """Add details of Flat if Flat not Present"""
    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']
        flat_no = request.form['flat_no']

        df = pd.DataFrame({'society_id': str(society_id), 'wing': str(wing_name), 'flat_no': str(flat_no)}, index=[0])

        with dbm.dbManager() as manager:
            manager.commit(df, 'visitor_management_schema.flat_details')
            success = True
            return jsonify(success)

    except psycopg2.DatabaseError as error:
        errors = {'get_wing_list': False, 'error': (error)}
        return str(errors)


@app.route('/get_flat_id', methods=['GET', 'POST'])
def get_flat_id():
    """get flat id by giving the society and flat no and wing name"""
    society_id = request.form['society_id']
    wing_name = request.form['wing_name']
    flat_no = request.form['flat_no']
    query_flat_id = queries['get_flat_id']

    query = query_flat_id.format(society_id, wing_name, flat_no)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query)

    return jsonify(result.to_dict(orient='records'))



@app.route('/user/register', methods=['GET','POST'])
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

    try:

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

        with dbm.dbManager() as manager:
            manager.commit(df, 'visitor_management_schema.user_table')
            return "User registered Successfully"
    except psycopg2.DatabaseError as error:
        errors = {'registeration': False, 'error': error}
        return str(errors)


@app.route('/user/register/staff', methods=['GET', 'POST'])
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


#staff Login
@app.route('/user/login', methods=['GET', 'POST'])
def login():
    logging.info("Running Login")
    validate_query = queries['user_login']
    
    username = request.form['username']
    password = request.form['password']
    user_login_query = validate_query.format(username, password)

    with dbm.dbManager() as manager:
            result = manager.getDataFrame(user_login_query)
            return jsonify(result.to_dict(orient='records'))


@app.route('/get_login_details', methods=['GET', 'POST'])
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

@app.route('/update_user_photo', methods=['GET','POST'])
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





# visitor entry from staff
@app.route('/insertVisitor', methods=['GET','POST'])
def insertVisitor():
    logging.debug("Running insertVisitor:")
    for key in verdict_visitor:
        try:
            verdict_visitor[key]=request.form[key]
        except:
            pass

    '''tuple format to send args to proc'''
    tuple_insert = tuple(verdict_visitor.values())
    logging.info("tuple_insert is : %s", tuple_insert)
    try:
        with dbm.dbManager() as manager:
            visitor_id = manager.callprocedure('visitor_management_schema.insertvisitor', tuple_insert)
            #result = manager.getDataFrame(query)
            logging.info('Visitor details entered successfully for id %s', visitor_id)
            return jsonify(visitor_id)

    except psycopg2.DatabaseError as error:
        errors = {'visitor_entry': False,
                  	'error': (error)
                  	}
        return str(errors)


@app.route('/update_visitor_exit',methods=['GET','POST'])
def update_visitor_exit():
    update_visitor_exit = queries['update_visitor_exit']
    visitor_id = request.form['id']
    exit_time = request.form['exit_time']
    try:
        update_query = update_visitor_exit.format(exit_time, visitor_id)
        
        with dbm.dbManager() as manager:
            manager.updateDB(update_query)
        success = True
    except:
        success = False
    return jsonify(success)
        

@app.route('/dashboard_count', methods=['GET','POST'])
def dashboard_count():
    try:
        society_id = request.form['society_id']
        query_society_id = queries['admin_dashboard']
        query = query_society_id.format(society_id,society_id)

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)

        return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'registration': False, 'error': error}
        return str(errors)


#admin access
@app.route('/dashboard_staff', methods=['GET', 'POST'])
def dashboard_staff():
    society_id = request.form['society_id']
    query_society_staff = queries['society_staff_list']

    query = query_society_staff.format(society_id)
    
    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query)

    return jsonify(result.to_dict(orient='records'))


@app.route('/dashboard_members', methods=['GET', 'POST'])
def dashboard_members():
    society_id = request.form['society_id']
    user_status = request.form['user_status']
    query_society_staff = queries['society_members_list']

    query = query_society_staff.format(user_status, society_id)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query)

    return jsonify(result.to_dict(orient='records'))


@app.route('/dashboard_visitor', methods=['GET', 'POST'])
def dashboard_visitor():
    society_id = request.form['society_id']
    all_visitor_details = queries['all_visitor_details3']
    query_visitor_list = all_visitor_details.format(society_id)
    
    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query_visitor_list)
        logging.info('Visitor details are %s', result)
        return result.to_json(orient='records')


@app.route('/get_flat_visitor_details', methods=['GET', 'POST'])
def get_flat_visitor_details():
    society_id = request.form['society_id']
    flat_id = request.form['flat_id']
    all_visitor_details = queries['flat_visitor_details']
    query_visitor_list = all_visitor_details.format(society_id, flat_id)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query_visitor_list)
        logging.info('Visitor details are %s', result)
        return result.to_json(orient='records')


@app.route('/user/set_user_login_status', methods=['GET', 'POST'])
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


@app.route('/user/set_user_admin_status', methods=['GET', 'POST'])
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


@app.route('/visitor/set_visitor_status', methods=['GET', 'POST'])
def set_visitor_status():
    logging.info("Called set_visitor_status")
    visitor_id = request.form['visitor_id']
    visitor_status = request.form['visitor_status']
    logging.info('Setting Visitor id: %s status set to %s', visitor_id, visitor_status)
    query_set_visitor_status = queries['set_visitor_status']

    set_approve_user_query = query_set_visitor_status.format(int(visitor_status), str(visitor_id))
    with dbm.dbManager() as manager:
        result = manager.updateDB(set_approve_user_query)
        logging.info('Visitor id: %s  status set to %s', visitor_id, visitor_status)
        return jsonify(bool(result))

app.run(debug=True)