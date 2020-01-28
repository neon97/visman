from peewee import IntegerField, CharField, IdentityField, DateTimeField,ForeignKeyField, TextField
from vis_app.Models.BaseModel import BaseModel
from vis_app.Models.Society import Society
from vis_app.Models.Flat import Flat
from vis_app.Models.User import User


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
    society_id = ForeignKeyField(Society, deferrable=True)
    user_id = ForeignKeyField(User, deferrable=True)
    visit_reason = CharField()
    photo = TextField()
    flat_id = ForeignKeyField(Flat, deferrable=True)
    whom_to_visit = ForeignKeyField(model=User, to_field=id, null=False, deferrable=True)
    whom_to_visit = IntegerField()
    visitor_status = IntegerField()
    vehicle = CharField()
    people_count = IntegerField()


    def serialize(self):
        """Serialize this object to dict/json."""
        d = super(Visitor, self).serialize()
        return d


    