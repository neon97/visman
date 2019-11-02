import psycopg2, config_parser
from flask import Flask, request, jsonify
import pandas as pd
import db_config.dbManager as dbm
import psycopg2, config_parser
from flask import Flask, request, jsonify
import pandas as pd
import db_config.dbManager as dbm


params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')

def society_info():
    """ Gives the society id and society name for all registered society."""
    try:
        query = queries['suggest_id_name']

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)

        print(result)
        #return jsonify(result.to_dict(orient='records'))

    except psycopg2.DatabaseError as error:
        errors = {'society info': False, 'error': error}
        return str(errors)


def get_id():
    """ get the society id by passing the society registration."""
    try:
        regd_no = 'mavi'
        query_society_id = queries['get_society_id']
        query = query_society_id.format(regd_no)

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)

        print(result.to_dict(orient='records'))
        #return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'registeration': False, 'error': (error)}
        return str(errors)


def dashboard_count():
    try:
        society_id = '2'
        query_society_id = queries['visitor_and_watchman_cnt']
        query = query_society_id.format(society_id)

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)

        #return result.to_dict(orient='records')
        return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'registeration': False, 'error': (error)}
        return str(errors)


#print(dashboard_count())


def dashboard_visitor():
    society_id = '2'
    all_visitor_details = queries['all_visitor_details']
    postgres_watchman = all_visitor_details.format(society_id)

    with dbm.dbManager() as manager:
        result = manager.getDataFrame(postgres_watchman)
        #result_Data = result.to_json(orient='values')
        result_Data = result.to_dict(orient='records')
        # result_Data = result.to_(orient='records')
        # result_type = type(jsonify(result_Data))

    return result_Data
    # return jsonify(result_Data)

print(dashboard_visitor())
#get_id()
#society_info()