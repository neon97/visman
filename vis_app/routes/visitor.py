from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

visitor = Blueprint('visitor', __name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')


"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
visitor_col = ['user_id', 'first_name', 'middle_name', 'last_name', 'contact_number', 'entry_time', 'people_count', 'society_id', 'flat_id',
               'visit_reason', 'visitor_status', 'whom_to_visit', 'vehicle', 'photo','otp']

verdict_visitor = {}

'''looping to check data type and prepare column value'''
for each_column in visitor_col:
    verdict_visitor[each_column] = None


# visitor entry from staff
@visitor.route('/insertVisitor', methods=['GET','POST'])
def insertVisitor():
    logging.debug("Running insertVisitor:")
    for key in verdict_visitor:
        logging.info("key is : %s", key)
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


@visitor.route('/update_visitor_exit',methods=['GET','POST'])
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


@visitor.route('/dashboard_visitor', methods=['GET', 'POST'])
def dashboard_visitor():
    society_id = request.form['society_id']
    all_visitor_details = queries['all_visitor_details3']
    query_visitor_list = all_visitor_details.format(society_id)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(query_visitor_list)
        logging.info('Visitor details are %s', result)
        return result.to_json(orient='records')


@visitor.route('/visitor/set_visitor_status', methods=['GET', 'POST'])
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

