#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 16:18:42 2019
@author: akshay72
"""
import psycopg2,config_parser
from flask import Flask , request,jsonify
import pandas as pd
import db_config.dbManager as dbm


start_time=""
end_time=""

app = Flask(__name__)
params = config_parser.config(filename='db_config/database.ini', section='postgresql')
queries = config_parser.config(filename='db_config/database.ini', section='queries')


def replace(data):
    if(data is not None):
        return data
    data=None
    return data


@app.route('/society_info',methods=['GET','POST'])
def society_info():
    try:
        query=queries['suggest_id_name']
        
        with dbm.dbManager() as manager:
            result=manager.getDataFrame(query)
        result_Data=result.to_json(orient='values')
        return result_Data
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
        
        with dbm.dbManager() as manager:
            result=manager.getDataFrame(query)
        result_Data=result.to_json(orient='values')
        return result_Data
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
                
        df=pd.DataFrame({'regd_no':regd_no,'building_name':building_name,'building_address':building_address,'total_buildings':total_buildings,'total_flats':total_flats},index=[0])     
        
        with dbm.dbManager() as manager:
            manager.commit(df,'visitor_management_schema.society_table')
        #first user details
        return "Society registered successfully"
    except psycopg2.DatabaseError as error:
        errors={'society registeration':False,
                 'error':(error)
                }
        return str(errors)
    
def generate(first,last):
    return first+last

#staff Registeration (staff may be watchman or secretary)
@app.route('/user/register', methods=['GET','POST'])
def user_register():
#    create_user=queries['create_user']
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
        
#        postgres_insert_query=create_user.format(str(username),str(email),str(first_name),str(middle_name),str(last_name),str(password),str(society_id),str(isadmin))
        
        df=pd.DataFrame({'username':str(username),'email':str(email),'first_name':str(first_name),'middle_name':str(middle_name),'last_name':str(last_name),'password':str(password),'society_id':str(society_id),'isadmin':str(isadmin)},index=[0])     

        with dbm.dbManager() as manager:
            manager.commit(df,'visitor_management_schema.user_table')
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
    
    with dbm.dbManager() as manager:
            result=manager.getDataFrame(postgres_user_login_query)
            result_Data=result.to_json(orient='values')

    return result_Data

# visitor entry from staff
@app.route('/insertVisitor',methods=['GET','POST'])
def visitor_entry():
#    insert_visitor=queries['insert_visitor']
    try:
        photo=request.form['photo']
        first_name=request.form['first_name']
        contact_number=request.form['contact_number']
        entry_time=request.form['entry_time']
        #entry_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flat_info=request.form['visiting_flat_no']
        last_name=replace(request.form['last_name'])
        staff_id=request.form['staff_id']
        visit_reason=request.form['visit_reason']
        society_id=request.form['society_id']
        
#        postgres_visitor_insert_query=insert_visitor.format(str(first_name),str(last_name),int(contact_number),str(entry_time),str(flat_info),int(staff_id),str(visit_reason),int(society_id),str(photo))
        
        df=pd.DataFrame({'first_name':str(first_name),'last_name':str(last_name),'contact_number':int(contact_number),'entry_time':str(entry_time),'flat_info':str(flat_info),'staff_id':int(staff_id),'visit_reason':str(visit_reason),'society_id':int(society_id),'photo':str(photo)},index=[0])     

        with dbm.dbManager() as manager:
            manager.commit(df,'visitor_management_schema.visitor_table')
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
        
        with dbm.dbManager() as manager:
            manager.updateDB(update_query)
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
    
    with dbm.dbManager() as manager:
        result=manager.getDataFrame(postgres_watchman_count)
        result_Data=result.to_json(orient='values')
        
        result1=manager.getDataFrame(postgres_visitor_count)
        result_Data1=result1.to_json(orient='values')

        
    return jsonify({'watchman_count':result_Data,'visitor_count':result_Data1})

#admin access
@app.route('/dashboard_watchman',methods=['GET','POST'])
def dashboard_watchman():
    admin_user=queries['non_admin_user']
    society_id=request.form['society_id']
    postgres_admin=admin_user.format(society_id)
    
    with dbm.dbManager() as manager:
        result=manager.getDataFrame(postgres_admin)
        result_Data=result.to_json(orient='values')
        
    return result_Data

@app.route('/dashboard_visitor',methods=['GET','POST'])
def dashboard_visitor():
    all_visitor_details=queries['all_visitor_details']
    society_id=request.form['society_id']
    postgres_watchman=all_visitor_details.format(society_id)
    
    with dbm.dbManager() as manager:
        result=manager.getDataFrame(postgres_watchman)
        result_Data=result.to_json(orient='values')
    
    return result_Data

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
    with dbm.dbManager() as manager:
        result=manager.getDataFrame('select * from visitor_management.test;')
        result_Data=result.to_json(orient='values')
#    cur.execute('select * from visitor_management.test;')
    return result_Data


