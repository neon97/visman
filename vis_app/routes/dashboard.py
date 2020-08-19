from flask import Flask, request, jsonify, Blueprint
from vis_app.Models.User import User
from vis_app.Models.Visitor import Visitor
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard_count', methods=['GET','POST'])
def dashboard_count():
    society_id = request.form['society_id']

    try:
        approved_members = User.select().where(User.society_id == society_id, User.user_entity == 1).count()
        unapproved_members = User.select().where(User.society_id == society_id, User.user_entity == -1 ).count()
        approved_staff = User.select().where(User.society_id == society_id, User.user_entity == -1 ).count()
        unapproved_staff = User.select().where(User.society_id == society_id, User.user_entity == -1 ).count()
        total_visitors = Visitor.select().where(Visitor.society_id == society_id).count()

        result = {'approved_members' : approved_members, 'unapproved_members':unapproved_members,
        'approved_staff': approved_staff,'unapproved_staff': unapproved_staff,'total_visitors': total_visitors}
   
        return jsonify(result)

    except Exception as error:
        logging.info(error)
        errors = {'dashboard_count retured ': False, 'error': error}
        return str(errors)



