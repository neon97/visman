from flask import Flask, request, jsonify, Blueprint
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser
from peewee import IntegrityError, DoesNotExist
from vis_app.routes.utils import query_to_json
logging.basicConfig(level=logging.DEBUG)
from vis_app.Models.User import User
from vis_app.Models.Society import Society
from vis_app.Models.Flat import Flat
from flask_bcrypt import Bcrypt
from vis_app.Models.BaseModel import db
from vis_app.Models.BaseModel import BaseModel
import json
from peewee import JOIN


start_time = ""
end_time = ""

user = Blueprint('user', __name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')

bcrypt = Bcrypt()

"""Columns in visitor table appended in  indicates column set to be None instead of string null"""
user_col = ['email', 'first_name', 'middle_name', 'last_name','password', 'contact_number', 'society_id', 
            'flat_id','isadmin','user_entity','photo']

# verdict_user = {}

# '''looping to check data type and prepare column value'''
# for each_column in user_col:
#     verdict_user[each_column] = None


@user.route('/user/register/staff', methods=['GET', 'POST'])
@user.route('/user/register', methods=['GET','POST'])
def user_register():
    """Society Member Registration """
    data = request.form
    return create_user(data)

    # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    

@user.route('/user/login', methods=['GET', 'POST'])
def login():
    logging.info("Running Login")
    username = request.form['username']
    password = request.form['password']

    try:
        user = User.get(User.username == username)
        logging.info('user is %s', user.username)
            #return 'Login successfull'
        if bcrypt.check_password_hash(user.password, password):
            #user.password == password:

             return 'Login successfull'
        else:
            return 'Login failed: Password does not mach'
    
    except User.DoesNotExist:
        return 'User does not exist'

    except Exception as error :
        errors = {'error': error}
        return str(errors)




def user_register_staff():
    """staff Registration (staff may be like watchman or society accounts guy)
    """

    try :
        email = request.form['email']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        password = request.form['password']
        society_id = request.form['society_id']
        isadmin = request.form['isadmin']
        user_status = request.form['user_status']
        identification_type = request.form['identification_type']
        identification_no = request.form['identification_no']
        identification_no = request.form['identification_no']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User()

        user.username = email
        user.email = email
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name= last_name
        user.password = hashed_password
        user.society_id = society_id
        user.isadmin = isadmin
        user.user_entity = user_status
        user.identification_type = identification_type
        user.identification_no = identification_no


        user.save()
        return 'User created successfully'
        
    except Exception as e:
        errors = {'User registration Failed , error is : ': e}
        return str(errors)



@user.route('/user/set/photo', methods=['GET','POST'])
@user.route('/update_user_photo', methods=['GET','POST'])
def update_user_photo():
    """
    update user photo
    requires user id
    """
    user_id = request.form['user_id']
    photo = request.form['photo']

    try:
        user = User.get(User.id == user_id)
        user.photo = photo
        user.save()
        success = True

    except User.DoesNotExist:
        return 'User does not exist'

    except Exception as error:
        logging.debug(error)
        success = False

    return jsonify(success)


@user.route('/user/set/login_status', methods=['GET', 'POST'])
@user.route('/user/set_user_login_status', methods=['GET', 'POST'])
def set_user_login_status():
    user_id = request.form['user_id']
    user_entity = request.form['user_status']
    logging.info('Setting User id: %s status set to %s', user_id, user_entity)
    try:
        user = User.get(User.id == user_id)
        user.user_entity = user_entity
        user.save()
        success = True

    except User.DoesNotExist:
        return 'User does not exist'

    except Exception as error:
        logging.debug(error)
        success = False

    return jsonify(success)


@user.route('/user/set/admin_status', methods=['GET', 'POST'])
@user.route('/user/set_user_admin_status', methods=['GET', 'POST'])
def set_user_admin_status():
    user_id = request.form['user_id']
    user_admin_status = request.form['user_admin_status']
    logging.info('Setting User id: %s status set to %s', user_id, user_admin_status)
    try:
        user = User.get(User.id == user_id)
        user.isadmin = user_admin_status
        user.save()
        success = True
    
    except User.DoesNotExist:
        return 'User does not exist'
        
    except Exception as error:
        logging.debug(error)
        success = False

    return jsonify(success)



@user.route('/get_login_details', methods=['GET', 'POST'])
def get_login_details():
    """
        get the details of user by the user id.
    """
    user_id = request.form['user_id']
    
    try:
        query = User.select(
            User.id,User.username, User.first_name,User.last_name
            , User.society_id, User.isadmin, User.user_entity, User.photo
            , Society.society_name, Flat.id
            , Flat.flat_no, Flat.wing).join(Society,JOIN.LEFT_OUTER
            ).join(Flat, JOIN.LEFT_OUTER, on=(User.flat_id == Flat.id)).where(User.id==user_id).dicts()
        
        return query_to_json(query)


        # if query.count() == 0 :
        #     return "No user found"
        # else:
        #     df = pd.DataFrame.from_dict(query) 
        #     result = df.to_json(orient='records')
        #     return Response(result,mimetype='application/json')

    except Exception as error :
        errors = {'error': error}
        return str(errors)


#admin access
@user.route('/dashboard_staff', methods=['GET', 'POST'])
def dashboard_staff():
    society_id = request.form['society_id']
    try:
        query = list(User.select().where(User.society_id==society_id, User.user_entity == 1 ).dicts()) 
        return query_to_json(query)

    except Exception as error :
        errors = {'error': error}
        return str(errors)


@user.route('/dashboard_members', methods=['GET', 'POST'])
def dashboard_members():
    society_id = request.form['society_id']
    user_status = request.form['user_status']
    
    try:
        query = list(User.select(
            User.id, User.first_name, User.middle_name, User.last_name
            , User.email, User.user_entity, User.isadmin
            , Flat.id, Flat.flat_no, Flat.wing
        ).join(Flat).where(User.society_id==society_id, User.user_entity == user_status).dicts()) 

        return query_to_json(query)

    except Exception as error :
        errors = {'error': error}
        return str(errors)


@user.route('/get_society_members_details', methods=['GET', 'POST'])
def get_society_members_details():
    """get list of wings from a Society"""
    try:
        society_id = request.form['society_id']
                
        query = list(User.select(User.first_name, User.last_name, Flat.id
        ,Flat.flat_no,Flat.wing
        ).join(Flat).where(User.user_entity == 1, User.society_id == society_id).dicts())


        return query_to_json(query)

    except Exception as error :
        errors = {'error': error}
        return str(errors)


def create_user(data):
     user = User()
    try:

        

        print(data)

        #user = User(**data)
        user.create(**data)
        #user.save()
        return jsonify(user.id)
    
    except Exception as error:
        
        logging.info(error)
        return str(error)