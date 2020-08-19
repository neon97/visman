import os
from playhouse.db_url import connect
import logging

DATABASE_URL = os.environ['DATABASE_URL']

# DATABASE_URL = 'postgresql://postgres:changeme@localhost:5433/visman'

# visman test database url
# DATABASE_URL = 'postgres://azqkdeiqpezmzj:ee1246a50f9c0d67038106e0557c7eddd05bdd0fda2149d831354388f53d70a9@ec2-54-235-250-38.compute-1.amazonaws.com:5432/d3u39l3sta71kl'


def db_connect():
    try:
        logging.info("Connecting to database {}".format(DATABASE_URL))    
        db = connect(DATABASE_URL, autorollback=True)
        logging.info("Database Connection Successful.")
        return db

    except Exception as error:
        return str(error)
