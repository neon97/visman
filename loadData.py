from vis_app.Models.Society import Society
from vis_app.Models.User import User
from vis_app.Models.Flat import Flat
import json
from vis_app.Models.db import db_connect
import db_config.dbManager as dbm

# db = db_connect()

delete_user_query = 'delete from visitor_management_schema.user_table'
delete_scoiety_query = 'delete from visitor_management_schema.society_table'
delete_flat_query = 'delete from  visitor_management_schema.flat_details;'


# with dbm.dbManager() as manager: 
#   manager.runSQL(delete_scoiety_query)
#   manager.runSQL('ALTER SEQUENCE visitor_management_schema.society_table_id_seq RESTART ')


with open('test_data/society.json') as f:
  data = json.load(f)
query = Society.insert_many(data)
query.execute()

with open('test_data/flat_details.json') as f:
  data = json.load(f)
query = Flat.insert_many(data)
query.execute()

with open('test_data/users.json') as f:
  data = json.load(f)
query = User.insert_many(data)
query.execute()



