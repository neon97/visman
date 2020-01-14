from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

flat = Blueprint('flat', __name__)

params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')


"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
visitor_col = ['user_id', 'first_name', 'middle_name', 'last_name', 'contact_number', 'entry_time', 'people_count', 'society_id', 'flat_id',
               'visit_reason', 'visitor_status', 'whom_to_visit', 'vehicle', 'photo','otp']

verdict_visitor = {}

'''looping to check data type and prepare column value'''
for each_column in visitor_col:
    verdict_visitor[each_column] = None


@flat.route('/get_wing_list', methods=['GET', 'POST'])
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


@flat.route('/get_flat_list', methods=['GET', 'POST'])
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


@flat.route('/add_flat', methods=['GET', 'POST'])
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


@flat.route('/get_flat_id', methods=['GET', 'POST'])
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

