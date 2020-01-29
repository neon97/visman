import os
from playhouse.db_url import connect

DATABASE_URL = os.environ['DATABASE_URL']

#DATABASE_URL = 'postgresql://postgres:changeme@localhost:5433/visman'

def db_connect():
    try:
        db = connect(DATABASE_URL, autorollback=True)
        return db
        
    except Exception as error:
        return str(error)
