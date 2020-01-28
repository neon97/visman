from flask import Flask, request, jsonify, Blueprint
from vis_app.Models.Society import Society
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

society = Blueprint('society', __name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')



@society.route('/society_register', methods=['GET', 'POST'])
def society_register():
    """Register society"""
    try:
        # society details
        regd_no = request.form['regd_no']
        society_name = request.form['society_name']
        society_address = request.form['society_address']
        total_buildings = request.form['total_buildings']
        total_flats = request.form['total_flats']

        society = Society()
        society.regd_no = regd_no
        society.society_name = society_name
        society.society_address = society_address
        society.total_buildings = total_buildings
        society.total_flats = total_flats

        society.save()

        success = True
        
        logging.info('Society registered successfully')
        

    except Exception as error:
        errors = {'society registeration': False,
                  'error': (error)
                  }
        logging.info(errors)
        success = False

    return jsonify(success)


@society.route('/get_society_id', methods=['GET', 'POST'])
def get_society_id():
    """ get the society id by passing the society registration."""
    try:
        regd_no = request.form['regd_no']
        #regd_no = request.form['regd_no']
        query_society_id = queries['get_society_id']
        query = query_society_id.format(regd_no)

        with dbm.dbManager() as manager:
            result = manager.getDataFrame(query)

        return jsonify(result.to_dict(orient='records'))
    except psycopg2.DatabaseError as error:
        errors = {'registeration': False, 'error': (error) }
        return str(errors)


@society.route('/society_info', methods=['GET', 'POST'])
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
