from flask import Flask, request, jsonify, Blueprint, Response
from vis_app.Models.Society import Society
import pandas as pd
import db_config.dbManager as dbm
import logging
import config_parser
from vis_app.routes.utils import result_to_json, CustResponseSend
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
    logging.info('Recievied Society Data {}'.format(data))
    return create_or_update(data)


@society.route('/society/get/id', methods=['GET', 'POST'])
@society.route('/get_society_id', methods=['GET', 'POST'])
# @login_required
def get_society_id():
    """ get the society id by passing the society registration."""
    try:
        regd_no = request.form['regd_no']
        query = Society.select(Society.id).where(Society.regd_no == regd_no)
        return result_to_json(query)
    except Exception as error:
        logging.info(error)
        return CustResponseSend("Error : {}".format(str(error)), False, [])


@society.route('/society/get/all', methods=['GET', 'POST'])
# @login_required
def society_info():
    """ Gives the society id and society name for all registered society."""
    query = Society.select()
    return  result_to_json(query)

def create_or_update(data):
    society = Society(**data)
    if 'id' in data:
        logging.info("Running update on Society :%s", society.id)
        try:
            logging.info("Getting Society info for id : {}".format(society.id))
            Society.get(id=society.id)
            society.save()
            return CustResponseSend("Update Successful", True, [{"id":society.id}])

        except Society.DoesNotExist as error:
            return CustResponseSend("Society does Not Exist", False, [])
            # return "User not found for id :{}".format(user.id)

        except Exception as error:
            return CustResponseSend("Error : {}".format(str(error)), False, [])
            # return error
    else:
        logging.info("Creating New Society : %s", society)
        try:
            logging.info("Cheking if Society registered with Regd No: {} exists".format(society.regd_no))
            society = Society.get(regd_no=society.regd_no)
            return CustResponseSend("Society with Regd No : {}, is already Registered".format(society.regd_no), False, [{"id":society.id}])
        except Society.DoesNotExist as error:
            logging.info('Society Does No exists, Creating New Society')
            logging.info(society)  
            try:
                society.save()
                logging.info("Society saved.")
                society = Society.select().where(Society.id == society.id)
                return  result_to_json(society)
            except Exception as error:
                logging.info(error)
                return CustResponseSend("Error : {}".format(str(error)), False, [])
                
        except Exception as error:
            logging.info(error)
            return CustResponseSend("Error : {}".format(str(error)), False, [])