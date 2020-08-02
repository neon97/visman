from flask import Flask, request, jsonify, Blueprint, Response
import json
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2
import config_parser
from vis_app.routes.utils import query_to_json,CustResponse
from .user import login_required

from vis_app.Models.Flat import Flat

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

flat = Blueprint('flat', __name__)

params = config_parser.config(
    filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(
    filename='db_config/database.ini', section='queries')

@flat.route('/flat/register', methods=['GET', 'POST'])
#@login_required
def add_flat():
    """Add details of Flat if Flat not Present"""
    try:
        data = request.form
        return create_or_update(data)

    except Exception as error:
        return CustResponse.send("Error : {}".format(str(error)), False, [])


@flat.route('/flat/get/id', methods=['GET', 'POST'])
#@login_required
def get_flat_id():
    logging.info("In function get_flat_id")
    """get flat id by giving the society and flat no and wing name"""

    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']
        flat_no = request.form['flat_no']
        logging.info("Recieved params : society_id : {}, wing_name : {}, flat_no : {}".format(society_id,wing_name,flat_no) )
    
        query = Flat.select().where(Flat.society_id == society_id,
                                    Flat.wing == wing_name, Flat.flat_no == flat_no)
        logging.debug("Running query : {}".format(query))
        result = query_to_json(query)
        logging.debug("Query Ran successfully")
        logging.info("Result is :{} ".format(result))
        return result

    except Exception as error:
        logging.info("Failed run query, Recieved Error: ")
        logging.info(error)
        return CustResponse.send("Error : {}".format(str(error)), False, [])

@flat.route('/society/get/wing/all', methods=['GET', 'POST'])
#@login_required
def get_wing_list():
    logging.info("In function get_wing_list")
    """get list of wings from a Society"""
    try:
        society_id = request.form['society_id']
        logging.info("Recieved society_id : {}".format(society_id))
        query = Flat.select(Flat.wing).where(
            Flat.society_id == society_id).distinct()
        logging.info("Running query: {}".format(query))
        result = query_to_json(query)
        logging.debug("Query Ran successfully")
        logging.info("Result is :{} ".format(result))
        return result

    except Exception as error:
        logging.info("Function get_wing_list Failed , Recieved Error: ")
        logging.info(error)
        return CustResponse.send("Error : {}".format(str(error)), False, [])

@flat.route('/society/get/flat/all', methods=['GET', 'POST'])
#@login_required
def get_flat_list():
    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']

        query = Flat.select(Flat.flat_no).where(
            Flat.society_id == society_id, Flat.wing == wing_name)
        result = query_to_json(query)
        return result

    except Exception as error:
        logging.info("Function get_flat_list Failed , Recieved Error: ")
        logging.info(error)
        return CustResponse.send("Error : {}".format(str(error)), False, [])


def create_or_update(data):
    logging.info("In function create_or_update")
    flat = Flat(**data)
    logging.info("Adding New Details  : %s", flat)
    try:
        flat.save_optimistic()
        logging.info("Flat details saved SUccessfully")
        new_flat = Flat.select(Flat.id).where(Flat.id == flat.id)
        return query_to_json(new_flat)
    except Exception as error:
        logging.info("Function create_or_update Failed , Recieved Error: ")
        logging.info(error)
        return CustResponse.send("Error : {}".format(str(error)), False, [])

