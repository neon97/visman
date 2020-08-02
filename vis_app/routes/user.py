from .utils import auth_user
from peewee import JOIN
import json
from vis_app.Models.BaseModel import BaseModel
from vis_app.Models.BaseModel import db
from flask_bcrypt import Bcrypt
from vis_app.Models.Flat import Flat
from vis_app.Models.Society import Society
from vis_app.Models.User import User
from flask import Flask, request, jsonify, Blueprint, session, flash, redirect, url_for
from functools import wraps
import db_config.dbManager as dbm
import logging
import psycopg2
import config_parser
from peewee import IntegrityError, DoesNotExist, fn
from vis_app.routes.utils import query_to_json, CustResponse
logging.basicConfig(level=logging.DEBUG)


start_time = ""
end_time = ""

user = Blueprint('user', __name__)
params = config_parser.config(
    filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(
    filename='db_config/database.ini', section='queries')

bcrypt = Bcrypt()


@user.route('/user/set/login_status', methods=['GET', 'POST'])
@user.route('/user/set/admin_status', methods=['GET', 'POST'])
@user.route('/user/set_user_admin_status', methods=['GET', 'POST'])
@user.route('/user/set/photo', methods=['GET', 'POST'])
@user.route('/user/register/staff', methods=['GET', 'POST'])
@user.route('/user/register', methods=['GET', 'POST'])
def user_register():
    logging.info("Infunction user_register")
    """Society Member Registration """
    data = request.form
    logging.info("Recieved data %s", data)
    return create_or_update(data)

    # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

# require to make intelligence for each user ##import required


def login_required(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            logging.info('session for user is running {}'.format(
                session.get('username')))
            return fn(*args, **kwargs)

        return 'Login required'
    return inner


@user.route('/user/login', methods=['GET', 'POST'])
def login():
    logging.info("Running Login")
    username = request.form['username']
    password = request.form['password']

    try:
        user = User.select().where(User.email == username).get()
        logging.info("username id %s", user.username)
        logging.info("user password is %s", user.password)
        if user.password == password:
            # validate true false
            query = User.select(User.id, User.username, User.first_name,
                                User.last_name, User.photo, User.user_entity, User.society_id,
                                User.isadmin,
                                User.flat_id, Flat.flat_no, Flat.wing,
                                Society.society_name).join(
                Flat, JOIN.LEFT_OUTER
            ).join(
                Society, JOIN.LEFT_OUTER
            ).where(User.id == user.id)
            auth_user(user)

            return query_to_json(query)

        else:
            logging.info("Function login Failed , Password does not mach, for User : %s",username)
            return CustResponse.send("Login failed: Password does not mach", False, [])

    except User.DoesNotExist as error:
        logging.info("Function login Failed , User : %s Does not exist ",username)
        return CustResponse.send("Error : {}".format(str(error)), False, [])

    except Exception as error:
        logging.info("Function login Failed , Recieved Error: ")
        logging.info(error)
        return CustResponse.send("Error : {}".format(str(error)), False, [])


@user.route('/user/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return 'Logged out '


@user.route('/user/get/id', methods=['GET', 'POST'])
@user.route('/get_login_details', methods=['GET', 'POST'])
# @login_required
def get_login_details():
    """
        get the details of user by the user id.
    """
    user_id = request.form['user_id']
    return get_user(user_id)


# admin access
@user.route('/dashboard_staff', methods=['GET', 'POST'])
# @login_required
def dashboard_staff():
    society_id = request.form['society_id']
    try:
        query1 = User.select().where(User.society_id == society_id, User.user_entity == 2)

        return query_to_json(query1)
    except Exception as error:
        return CustResponse.send("Error : {}".format(str(error)), False, [])


@user.route('/dashboard_members', methods=['GET', 'POST'])
# @login_required
def dashboard_members():
    society_id = request.form['society_id']
    user_status = request.form['user_status']

    try:
        query = User.select(
            User.id, User.first_name, User.middle_name, User.last_name, User.email, User.user_entity, User.isadmin, User.flat_id, Flat.flat_no, Flat.wing
        ).join(Flat, JOIN.LEFT_OUTER).where(User.society_id == society_id, User.user_entity == user_status)

        return query_to_json(query)

    except Exception as error:
        return CustResponse.send("Error : {}".format(str(error)), False, [])


@user.route('/get_society_members_details', methods=['GET', 'POST'])
# @login_required
def get_society_members_details():
    """get list of wings from a Society"""
    try:
        society_id = request.form['society_id']

        query = User.select(User.first_name.concat(" ").concat(User.last_name).alias('member'),
                            Flat.id, Flat.flat_no, Flat.wing
                            ).join(Flat).where(
            User.user_entity == 1, User.society_id == society_id
        )
        return query_to_json(query)

    except Exception as error:

        return CustResponse.send("Error : {}".format(str(error)), False, [])


def create_or_update(data):
    logging.info("In Function create_or_update()")
    user = User(**data)
    logging.info("User : %s", user)
    # print("User")
    if 'id' in data:
        logging.info("Running update on user :%s", user.id)
        try:
            logging.info("Getting User for id : %s", user.id)
            User.get(id=user.id)
            user.save()
            return CustResponse.send("Update Successful", True, [{ "id" : user.id}])

        except User.DoesNotExist as error:
            return CustResponse.send("Error : {}".format(str(error)), False, [])
            # return "User not found for id :{}".format(user.id)

        except Exception as error:
            return CustResponse.send("Error : {}".format(str(error)), False, [])
            # return error
    else:
        logging.info("Creating user : %s", user)
        user.username = user.email
        logging.info("Settting username as User Email :%s", user.username)
        try:
            logging.info("Cheking if email {} exists".format(user.email))
            user = User.get(email=user.email)
            return CustResponse.send("Email already used", False, [{"email:":user.email}])
        except User.DoesNotExist as error:
            logging.info('User Does No exists, Creating a New User')
            logging.info(user)

            try:
                logging.info('Saving User details:')
                logging.info("email: {}, firstname: {}, middlename: {}, lastname:{}, password: {}, society_id: {}, flat_id:{} , isadmin: {}, user_entity: {}".format(
                    user.email, user.first_name, user.middle_name, user.last_name, user.password, user.society_id, user.flat_id, user.isadmin, user.user_entity))
                user.save()
                logging.info("User saved.")
            except Exception as error:
                logging.info(error)
                return CustResponse.send("Error : {}".format(str(error)), False, [])
                
            user = User.select(User.id).where(User.id == user.id)
            return query_to_json(user)

        except Exception as error:
            logging.info(error)
            return CustResponse.send("Error : {}".format(str(error)), False, [])


def get_user(id):
    try:
        query = User.select(
            User.id,
            User.username,
            User.first_name,
            User.last_name,
            User.flat_id,
            User.society_id,
            User.isadmin, User.user_entity,
            User.photo,
            Society.society_name,
            Flat.id, Flat.flat_no,
            Flat.wing
        ).join(Society, JOIN.LEFT_OUTER
               ).join(Flat, JOIN.LEFT_OUTER, on=(User.flat_id == Flat.id)
                      ).where(User.id == id)
        return query_to_json(query)

    except Exception as error:
        logging.info("Function get_user failed with error : {}".format(str(error)))
        return CustResponse.send("Error : {}".format(str(error)), False, [])

