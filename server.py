#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 16:18:42 2019
@author: akshay72
"""
import psycopg2,config_parser
from flask import Flask , request,jsonify

start_time=""
end_time=""

app = Flask(__name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')

try:
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params,autocommit=True)
    cur = conn.cursor()
except  psycopg2.DatabaseError as error:
     jsonify(error)


def replace(data):
    if(data is not None):
        return data
    data=None
    return data


@app.route('/society_info',methods=['GET','POST'])
def society_info():
    try:
        query=queries['suggest_id_name']
        cur.execute(query)
        result=cur.fetchall()
        return jsonify(result)
    except psycopg2.DatabaseError as error:
        errors={'society info':False,
                 'error':(error)
                }
        return str(errors)
        

    
        
@app.route('/get_id',methods=['GET','POST'])
def get_id():
    try:
        regd_no=request.form['regd_no']
        query_society_id=queries['get_society_id']
        query=query_society_id.format(regd_no)
        cur.execute(query)
        conn.commit()
        return jsonify(cur.fetchone())
    except psycopg2.DatabaseError as error:
        errors={'registeration':False,
                 'error':(error)
                }
        return str(errors)

        
@app.route('/society_register', methods=['GET','POST'])
def society_register():
    try:
        #society details
        regd_no=request.form['regd_no']
        building_name=request.form['society_name']
        building_address=request.form['society_address']
        total_buildings=request.form['total_buildings']
        total_flats=request.form['total_flats']
        society_register_query=queries['society_register']
        query=society_register_query.format(str(regd_no),str(building_name),str(building_address),int(total_buildings),int(total_flats))
        cur.execute(query)
        #first user details
        return jsonify("society registered succesfully")
    except psycopg2.DatabaseError as error:
        errors={'society registeration':False,
                 'error':(error)
                }
        return str(errors)
    
def generate(first,last):
    return first+last

#staff Registeration (staff may be watchman or secretary)
@app.route('/user/register', methods=['GET','POST'])
def register():
    create_user=queries['create_user']
    try:
        #username=request.form['username']
        email=request.form['email']
        first_name=request.form['first_name']
        middle_name=request.form['middle_name']
        last_name=request.form['last_name']
        password=request.form['password']
        society_id=request.form['society_id']
        isadmin=request.form['isadmin']
        username=generate(first_name,last_name)
        postgres_insert_query=create_user.format(str(username),str(email),str(first_name),str(middle_name),str(last_name),str(password),str(society_id),str(isadmin))
        cur.execute(postgres_insert_query)
        conn.commit()
        return "User registered Succesfully"
    except psycopg2.DatabaseError as error:
        errors={'registeration':False,
                 'error':(error)
                }
        return str(errors)

#staff Login
@app.route('/user/login',methods=['GET','POST'])
def login():
    validate_query=queries['validate_user']
    
    username=request.form['email']
    password=request.form['password']
    postgres_user_login_query=validate_query.format(username,password)
    cur.execute(postgres_user_login_query)
    return jsonify(cur.fetchone())

# visitor entry from staff
@app.route('/insertVisitor',methods=['GET','POST'])
def visitor_entry():
    insert_visitor=queries['insert_visitor']
    try:
        first_name=request.form['first_name']
        contact_number=request.form['contact_number']
        entry_time=request.form['entry_time']
        #entry_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flat_info=request.form['visiting_flat_no']
        last_name=replace(request.form['last_name'])
        #middle_name=replace(request.form['middle_name'])
        staff_name=request.form['staff_id']
        visit_reason=request.form['visit_reason']
        society_id=request.form['society_id']
        postgres_visitor_insert_query=insert_visitor.format(str(first_name),str(last_name),int(contact_number),str(entry_time),str(flat_info),int(staff_name),str(visit_reason),int(society_id))
        cur.execute(postgres_visitor_insert_query)
        success=True
        return jsonify(success)

    except psycopg2.DatabaseError as error:
        errors={'visitor_entry':False,
             'error':(error)
              }
        return str(errors)
    # middle_name ,contact_number ,flat_info

@app.route('/update_exit',methods=['GET','POST'])
def update_exit():
    #update_exit=queries['update_exit']
    visitor_id=request.form['id']
    exit_time=request.form['exit_time']
    try:
        update_query='''update visitor_management_schema.visitor_table set exit_time='{}' where id={}'''.format(exit_time,visitor_id)
        cur.execute(update_query)
        success=True
    except: 
        success=False
    return jsonify(success)
        

# admin access
@app.route('/dashboard_count',methods=['GET','POST'])
def dashboard_data():
    non_admin_user=queries['non_admin_user_count']
    total_visitor_count=queries['total_visitor_count']
    society_id=request.form['society_id']
    postgres_visitor_count=total_visitor_count.format(society_id)
    postgres_watchman_count=non_admin_user.format(society_id)
    cur.execute(postgres_watchman_count)
    watchman_count=cur.fetchone()
    cur.execute(postgres_visitor_count)
    visitor_count=cur.fetchone()
    return jsonify({'watchman_count':watchman_count[0],'visitor_count':visitor_count[0]})

#admin access
@app.route('/dashboard_watchman',methods=['GET','POST'])
def dashboard_watchman():
    admin_user=queries['non_admin_user']
    society_id=request.form['society_id']
    postgres_admin=admin_user.format(society_id)
    cur.execute(postgres_admin)
    user=cur.fetchall()
    return jsonify({'user':user})

@app.route('/dashboard_visitor',methods=['GET','POST'])
def dashboard_visitor():
    all_visitor_details=queries['all_visitor_details']
    society_id=request.form['society_id']
    postgres_watchman=all_visitor_details.format(society_id)
    cur.execute(postgres_watchman)
    user=cur.fetchall()
    return jsonify({'user':(user)})
    
@app.route('/',methods=['GET','POST'])
def hello_worlds():
    return "<div><b>Sorry!!<br/>only team has accesss to database<b><a href='/about'>About</a></div>"
    

@app.route('/mayur',methods=['GET','POST'])
def hello_world():
    return "<div><b>Hello World! This is Mayur mia<b></div>"

@app.route('/mia',methods=['GET','POST'])
def hello():
    return "Hello World! This is Akshay mia"

@app.route('/raj',methods=['GET','POST'])
def hellos():
    return "Hello World! This is Raj mia"

@app.route('/about',methods=['GET','POST'])
def about():
    return jsonify({'Company':'Visitor Management',
                    'Dev center':'Team Foundation',
                    'version':'heroku test development'})

@app.route('/id',methods=['GET','POST'])
def helloid():
    cur.execute('select * from visitor_management.test;')
    result=cur.fetchall()
    return jsonify(result)  

