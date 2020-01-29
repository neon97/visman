from flask import Flask, request, jsonify, Blueprint
from vis_app.Models.Society import Society
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser
from vis_app.routes.utils import query_to_json

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

society = Blueprint('society', __name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')



@society.route('/society_register', methods=['GET', 'POST'])
def society_register():
    """Register society"""
    data = request.form
    return create_or_update(data)

@society.route('/get_society_id', methods=['GET', 'POST'])
def get_society_id():
    """ get the society id by passing the society registration."""
    try:
        regd_no = request.form['regd_no']
        query = Society.select(Society.id).where(Society.regd_no == regd_no)
        
        return query_to_json(query)

    except Exception as error:
        logging.info(error)
        return str(error)


@society.route('/society_info', methods=['GET', 'POST'])
def society_info():
    """ Gives the society id and society name for all registered society."""
    try:
        query = Society.select()
        return query_to_json(query)

    except  Exception as error:
        logging.info(error)
        return str(error)


def create_or_update(data):
    try:
        society = Society(**data)
        society.save()
        return jsonify(society.id)
    
    except Exception as error:

        logging.info(error)
        return str(error)