import os
from playhouse.db_url import connect
import logging

# DATABASE_URL = os.environ['DATABASE_URL']

# DATABASE_URL = 'postgresql://postgres:changeme@localhost:5433/visman'

# visman test database url
# DATABASE_URL = 'postgres://azqkdeiqpezmzj:ee1246a50f9c0d67038106e0557c7eddd05bdd0fda2149d831354388f53d70a9@ec2-54-235-250-38.compute-1.amazonaws.com:5432/d3u39l3sta71kl'

# visman prod database url
DATABASE_URL = 'postgres://gawsmrxbzfvrmf:4e011cd366dd047014b1e42fa8992a6e4eeabc164f21053a37435a8b5ee4b289@ec2-54-227-251-33.compute-1.amazonaws.com:5432/d5267ba9erjt2u'

#data loding and restarting
# ALTER SEQUENCE visitor_management_schema.visitor_table_id_seq RESTART;
# ALTER SEQUENCE visitor_management_schema.user_table_id_seq RESTART;
# ALTER SEQUENCE visitor_management_schema.flat_details_id_seq RESTART;
# ALTER SEQUENCE visitor_management_schema.society_table_id_seq RESTART;


def db_connect():
    try:
        logging.info("Connecting to database {}".format(DATABASE_URL))    
        db = connect(DATABASE_URL, autorollback=True)
        logging.info("Database Connection Successful.")
        return db

    except Exception as error:
        return str(error)


