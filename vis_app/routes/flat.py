from flask import Flask, request, jsonify, Blueprint, Response
import json
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser

from vis_app.Models.Flat import Flat

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

flat = Blueprint('flat', __name__)

params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')



@flat.route('/add_flat', methods=['GET', 'POST'])
def add_flat():
    """Add details of Flat if Flat not Present"""
    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']
        flat_no = request.form['flat_no']

        flat = Flat()

        flat.flat_no = flat_no
        flat.wing = wing_name
        flat.society_id = society_id

        flat.save()
        
        return 'Flat added successfully'

    except psycopg2.errors.UniqueViolation as e:
            return 'Flat already exists.'       

    except Exception as e:
        errors = {'Flat registration Failed , error is : ': e}
        return str(errors)

@flat.route('/get_flat_id', methods=['GET', 'POST'])
def get_flat_id():
    """get flat id by giving the society and flat no and wing name"""
    
    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']
        flat_no = request.form['flat_no']
        
        data = list(Flat.select().where(Flat.society_id == society_id, Flat.wing == wing_name, Flat.flat_no == flat_no ).dicts())
        result = Response(json.dumps(data), mimetype='application/json')
        return result

    except Exception as error :
        errors = {'error': error}
        return str(errors)



@flat.route('/get_wing_list', methods=['GET', 'POST'])
def get_wing_list():
    """get list of wings from a Society"""
    try:
        society_id = request.form['society_id']

        data = list(Flat.select(Flat.wing).where(Flat.society_id == society_id).distinct().dicts())
        result = Response(json.dumps(data), mimetype='application/json')
        return result

    except Exception as error :
        errors = {'error': error}
        return str(errors)


@flat.route('/get_flat_list', methods=['GET', 'POST'])
def get_flat_list():
    try:
        society_id = request.form['society_id']
        wing_name = request.form['wing_name']
   
        data = list(Flat.select(Flat.flat_no).where(Flat.society_id == society_id, Flat.wing == wing_name ).dicts())
        result = Response(json.dumps(data), mimetype='application/json')
        return result

    except Exception as error :
        errors = {'error': error}
        return str(errors)


