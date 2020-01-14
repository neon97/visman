from peewee import *
from vis_app.Models.BaseModel import BaseModel
from vis_app.Models.Society import Society

class Flat(BaseModel):
    class Meta:
        db_table = 'flat_details'

    id = IdentityField()
    flat_no = IntegerField()
    wing = CharField()
    society_id = ForeignKeyField(Society)