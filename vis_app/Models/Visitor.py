from peewee import *
from vis_app.Models.BaseModel import BaseModel


class Visitor(BaseModel):
    class Meta:
        db_table='visitor_table'

    id = IdentityField()
    first_name = CharField()
    middle_name = CharField()
    last_name = CharField()
    contact_number = CharField()
    entry_time =  DateTimeField()
    exit_time = DateTimeField()
    society_id = ForeignKeyField(Society, lazy_load=True)
    user_id = ForeignKeyField(User, lazy_load=True)
    visit_reaason = CharFeild()
    photo = TextField()
    flat_id = ForeignKeyField(Flat, lazy_load=True)
    visitor_status = IntegerField()
    vehical = CharFeild()
    people_count = IntegerField()
    whom_to_visit = ForeignKeyField(User, lazy_load=True)