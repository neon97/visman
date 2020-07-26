from flask import Flask, request, jsonify, Blueprint, Response
from vis_app.Models.Society import Society
import pandas as pd
import db_config.dbManager as dbm
import logging
import config_parser
from vis_app.routes.utils import query_to_json, CustResponse
from .user import login_required

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

society = Blueprint('society', __name__)
params = config_parser.config(
    filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(
    filename='db_config/database.ini', section='queries')


@society.route('/society/register', methods=['GET', 'POST'])
@society.route('/society_register', methods=['GET', 'POST'])
# @login_required
def society_register():
    """Register society"""
    data = request.form
    return create_or_update(data)


@society.route('/get_society_id', methods=['GET', 'POST'])
# @login_required
def get_society_id():
    """ get the society id by passing the society registration."""
    try:
        regd_no = request.form['regd_no']
        query = Society.select(Society.id).where(Society.regd_no == regd_no)

        return CustResponse.send("Succesful", True, query_to_json(query))

    except Exception as error:
        logging.info(error)
        return CustResponse.send("UnSuccesful", False, str(error))


@society.route('/society/get/all', methods=['GET', 'POST'])
# @login_required
def society_info():
    """ Gives the society id and society name for all registered society."""
    try:
        query = Society.select()
        return CustResponse.send("Succesful", True, query_to_json(query))
        # return query_to_json(query)
    except Exception as error:
        logging.info(error)
        return CustResponse.send("UnSuccesful", False, str(error))


def create_or_update(data):
    try:
        society = Society(**data)
        society.save()
        return CustResponse.send("Succesful", True, str(society.id))
        # return jsonify(society.id)

    except Exception as error:

        logging.info(error)
        return CustResponse.send("UnSuccesful", False, str(error))
        # return str(error)
