from flask import Flask, request, jsonify, Blueprint, Response
import json
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2
import config_parser
from vis_app.routes.utils import query_to_json
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


@flat.route('/add_flat', methods=['GET', 'POST'])
@login_required
def add_flat():
    """Add details of Flat if Flat not Present"""
    try:
        data = request.form
        return create_or_update(data)

    except Exception as error:
        return str(error)


@flat.route('/get_flat_id', methods=['GET', 'POST'])
@login_required
def get_flat_id():
    """get flat id by giving the society and flat no and wing name"""

    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']
        flat_no = request.form['flat_no']

        query = Flat.select().where(Flat.society_id == society_id,
                                    Flat.wing == wing_name, Flat.flat_no == flat_no)
        result = query_to_json(query)
        return result

    except Exception as error:
        errors = {'error': error}
        return str(errors)


@flat.route('/get_wing_list', methods=['GET', 'POST'])
@login_required
def get_wing_list():
    """get list of wings from a Society"""
    try:
        society_id = request.form['society_id']

        query = Flat.select(Flat.wing).where(
            Flat.society_id == society_id).distinct()
        result = query_to_json(query)
        return result

    except Exception as error:
        errors = {'error': error}
        return str(errors)


@flat.route('/get_flat_list', methods=['GET', 'POST'])
@login_required
def get_flat_list():
    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']

        query = Flat.select(Flat.flat_no).where(
            Flat.society_id == society_id, Flat.wing == wing_name)
        result = query_to_json(query)
        return result

    except Exception as error:
        errors = {'error': error}
        return str(errors)


def create_or_update(data):
    try:
        flat = Flat(**data)
        flat.save()
        return jsonify(flat.id)

    except Exception as error:

        logging.info(error)
        return str(error)
