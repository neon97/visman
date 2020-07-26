from vis_app.Models.Society import Society
from vis_app.Models.User import User
from vis_app.Models.Flat import Flat
import json
from vis_app.Models.db import db_connect



with open('test_data/society.json') as f:
  data = json.load(f)

query = Society.insert_many(data)
query.execute()

with open('test_data/users.json') as f:
  data = json.load(f)
query = User.insert_many(data)
query.execute()

with open('test_data/flat_details.json') as f:
  data = json.load(f)
query = Flat.insert_many(data)
query.execute()



# scoiety_feilds = [Society.regd_no, Society.society_name, Society.society_address, Society.total_flats, Society.total_buildings]
# with db.atomic():
#     Society.insert_many(scoiety_data, fields=scoiety_feilds).execute()

# society = Society()
# society.regd_no = 1
# society.society_name = ''
# society.save()