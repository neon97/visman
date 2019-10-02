from flask import Flask,jsonify


app = Flask(__name__)

#@app.route('/',methods=['GET','POST'])
#def hello_world():
    #return "Hello World! This is mayur"

@app.route('/mayur',methods=['GET','POST'])
def hello_world():
    return "Hello World! This is Mayur mia"

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