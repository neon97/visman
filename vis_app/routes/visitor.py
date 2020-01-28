from flask import Flask, request, jsonify, Blueprint, Response
from peewee import * 
import json
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser
from vis_app.Models.Visitor import Visitor
from playhouse.shortcuts import model_to_dict


logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

visitor = Blueprint('visitor', __name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')


"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
visitor_col = ['userid', 'first_name', 'middle_name', 'last_name', 'contact_number', 'entry_time', 'people_count', 'society_id', 'flat_id',
               'visit_reason', 'visitor_status', 'whom_to_visit', 'vehicle', 'photo']

verdict_visitor = {}

'''looping to check data type and prepare column value'''
for each_column in visitor_col:
    verdict_visitor[each_column] = None


# visitor entry from staff
@visitor.route('/insertVisitor', methods=['GET','POST'])
def insertVisitor():
    logging.debug("Running insertVisitor:")
    for key in verdict_visitor:
        #logging.info("key is : %s", key)
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
            logging.info('Visitor details entered successfully for id %s', visitor_id)
            return jsonify(visitor_id)

    except psycopg2.DatabaseError as error:
        errors = {'visitor_entry': False,
                  	'error': (error)
                  	}
        return str(errors)


@visitor.route('/update_visitor_exit',methods=['GET','POST'])
def update_visitor_exit():
    visitor_id = request.form['id']
    exit_time = request.form['exit_time']
    try:
        visitor = Visitor.get(Visitor.id == visitor_id)
        visitor.exit_time = exit_time
        visitor.save()
        success = True

    except Visitor.DoesNotExist:
        return 'User does not exist'
    except:
        success = False
    return jsonify(success)



@visitor.route('/visitor/set_visitor_status', methods=['GET', 'POST'])
def set_visitor_status():
    logging.info("Called set_visitor_status")
    visitor_id = request.form['visitor_id']
    visitor_status = request.form['visitor_status']
    logging.info('Setting Visitor id: %s status set to %s', visitor_id, visitor_status)

    try:
        visitor = Visitor.get(Visitor.id == visitor_id)
        visitor.visitor_status = visitor_status
        visitor.save()
        success = True

    except Visitor.DoesNotExist:
        return 'User does not exist'
    except:
        success = False
    return jsonify(success)



@visitor.route('/dashboard_visitor', methods=['GET', 'POST'])
def dashboard_visitor():
    society_id = request.form['society_id']
    try:
        visitors = Visitor.select().where(Visitor.society_id  == society_id).dicts()
        if visitors.count() == 0 :
            return "No visitors found"
        else:
            df = pd.DataFrame.from_dict(visitors) 
            result = df.to_json(orient='records')
            return Response(result,mimetype='application/json')

    except Exception as error :
        errors = {'error': error}
        return str(errors)


@visitor.route('/get_flat_visitor_details', methods=['GET', 'POST'])
def get_flat_visitor_details():
    society_id = request.form['society_id']
    flat_id = request.form['flat_id']

    try:
        visitors = Visitor.select().where(Visitor.society_id == society_id, Visitor.flat_id == flat_id).dicts()
        if visitors.count() == 0 :
            return "No visitors found"
        else:
            df = pd.DataFrame.from_dict(visitors) 
            result = df.to_json(orient='records')
            return Response(result,mimetype='application/json')

    except Exception as error :
        errors = {'error': error}
        logging.info(errors)
        return str(errors)



