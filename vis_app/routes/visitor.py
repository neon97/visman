from flask import Flask, request, jsonify, Blueprint, Response
import json
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2
import config_parser
from vis_app.Models.Visitor import Visitor
from vis_app.Models.Flat import Flat
from vis_app.Models.User import User
from vis_app.Models.Flat import Flat
from vis_app.Models.BaseModel import BaseModel
from playhouse.shortcuts import model_to_dict
from vis_app.routes.utils import query_to_json1
from vis_app.routes.utils import query_to_json,CustResponse
from .user import login_required



logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

visitor = Blueprint('visitor', __name__)
params = config_parser.config(
    filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(
    filename='db_config/database.ini', section='queries')


"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
visitor_col = ['userid', 'first_name', 'middle_name', 'last_name', 'contact_number', 'entry_time', 'people_count', 'society_id', 'flat_id',
               'visit_reason', 'visitor_status', 'visit_user_id', 'vehicle', 'photo']

verdict_visitor = {}

'''looping to check data type and prepare column value'''
for each_column in visitor_col:
    verdict_visitor[each_column] = None


# visitor entry from staff
@visitor.route('/insertVisitor', methods=['GET', 'POST'])
@visitor.route('/visitor/insert', methods=['GET', 'POST'])
#@login_required
def create_or_update_visitor():
    logging.debug("Running function create_or_update_visitor:")
    try:
        data = request.form
        return create_or_update(data)
    except Exception as error:
        return CustResponse.send("Error : {}".format(str(error)), False, [])


@visitor.route('/dashboard_visitor', methods=['GET', 'POST'])
#@login_required
def dashboard_visitor():
    society_id = request.form['society_id']
    try:
        # query = Visitor.select().where(Visitor.society_id  == society_id).dicts()
        #
        query = Visitor.select(
            Visitor.id.alias('visitor_id'), Visitor.first_name.alias('visitor_first_name'), Visitor.last_name.alias('visitor_last_name'), Visitor.contact_number.alias(
                'visitor_contact_number'), Visitor.user_id, Visitor.visit_reason, Visitor.photo.alias('visitor_photo'), Visitor.visit_reason, Visitor.visitor_status, Visitor.entry_time, Visitor.exit_time,
            User.first_name.alias('staff_first_name'), User.last_name.alias(
                'staff_last_name'),
            Flat.flat_no, Flat.wing
        ).join(User,
               on=(Visitor.user_id == User.id)).join(Flat
                                                     #,on=(Visitor.flat_id == Flat.id)
                                                     ).where(Visitor.society_id == society_id)
        return query_to_json(query)
    except Exception as error:
        logging.info(error)
        return CustResponse.send("Error : {}".format(str(error)), False, [])

@visitor.route('/flat/visitor/details', methods=['GET', 'POST'])
@visitor.route('/get_flat_visitor_details', methods=['GET', 'POST'])
#@login_required
def get_flat_visitor_details():
    logging.info("In Function get_flat_visitor_details().")
    society_id = request.form['society_id']
    flat_id = request.form['flat_id']
    logging.info("Recieved params - society_id : {}, flat_id :{}".format(society_id, flat_id))
    try:
        query = Visitor.select(Visitor.id.alias('visitor_id'),
        Visitor.first_name.alias('visitor_first_name'),
        Visitor.middle_name.alias('visitor_middle_name'),
        Visitor.last_name.alias('visitor_last_name'),
        Visitor.contact_number.alias('visitor_contact_number'),
        Visitor.photo.alias('visitor_photo'),
        Visitor.visit_reason,Visitor.society_id, Visitor.visitor_status, Visitor.user_id,
        Visitor.entry_time, Visitor.exit_time, Visitor.flat_id, Visitor.visit_user_id,
        Visitor.people_count, Visitor.vehicle,
        Flat.wing, Flat.flat_no
        ).join(Flat).where(Visitor.society_id == society_id, Visitor.flat_id == flat_id)
        return query_to_json(query)

    except Exception as error:
        errors = {'error': error}
        logging.info(errors)
        return CustResponse.send("Error : {}".format(str(error)), False, [])


def create_or_update(data):
    try:
        logging.info("With data: %s", data)
        visitor = Visitor(**data)
        visitor.save()
        visitor = Visitor.select(Visitor.id).where(Visitor.id == visitor.id)
        return query_to_json(visitor)
        # return CustResponse.send("UnSuccessful:Failed to register Visitor", True, str(visitor.id))

    except Exception as error:
        logging.info(error)
        return CustResponse.send("Error : {}".format(str(error)), False, [])

@visitor.route('/vistter/set/visitor_exit', methods=['GET', 'POST'])
@visitor.route('/update_visitor_exit', methods=['GET', 'POST'])
def update_visitor_exit():

    visitor_id = request.form['id']
    exit_time = request.form['exit_time']
    try:
        visitor = Visitor.get(Visitor.id == visitor_id)
        visitor.exit_time = exit_time
        visitor.save()
        visitor = Visitor.select().where(Visitor.id == visitor.id)
        return  query_to_json(visitor)

    except Visitor.DoesNotExist:
        return CustResponse.send("Visitor does not exist", False, [])
        # return 'User does not exist'
    except Exception as error :
        return CustResponse.send("Error : {}".format(str(error)), False, [])
    


@visitor.route('/visitor/set/visitor_status', methods=['GET', 'POST'])
@visitor.route('/visitor/set_visitor_status', methods=['GET', 'POST'])
def set_visitor_status():
    logging.info("Called set_visitor_status")
    visitor_id = request.form['visitor_id']
    visitor_status = request.form['visitor_status']
    logging.info('Setting Visitor id: %s status set to %s',
                 visitor_id, visitor_status)

    try:
        visitor = Visitor.get(Visitor.id == visitor_id)
        visitor.visitor_status = visitor_status
        visitor.save()
        visitor = Visitor.select().where(Visitor.id == visitor.id)
        return  query_to_json(visitor)

    except Visitor.DoesNotExist :
        return CustResponse.send("Visitor does not exist", False, [])
        # return 'User does not exist'
    except Exception as error :
        return CustResponse.send("Error : {}".format(str(error)), False, [])
   
