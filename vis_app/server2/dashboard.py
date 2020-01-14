from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

dashboard = Blueprint('dashboard', __name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')


"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
visitor_col = ['user_id', 'first_name', 'middle_name', 'last_name', 'contact_number', 'entry_time', 'people_count', 'society_id', 'flat_id',
               'visit_reason', 'visitor_status', 'whom_to_visit', 'vehicle', 'photo','otp']

verdict_visitor = {}

'''looping to check data type and prepare column value'''
for each_column in visitor_col:
    verdict_visitor[each_column] = None

@server.route('/dashboard_count', methods=['GET','POST'])
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


@server.route('/get_flat_visitor_details', methods=['GET', 'POST'])
def get_flat_visitor_details():
    society_id = request.form['society_id']
    flat_id = request.form['flat_id']
    all_visitor_details = queries['flat_visitor_details']
    query_visitor_list = all_visitor_details.format(society_id, flat_id)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query_visitor_list)
        logging.info('Visitor details are %s', result)
        return result.to_json(orient='records')

