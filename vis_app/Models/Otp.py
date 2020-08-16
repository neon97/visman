from peewee import IdentityField,IntegerField,DateTimeField,CharField,ForeignKeyField
from vis_app.Models import User,Visitor
from vis_app.Models.BaseModel import BaseModel


class OTP(BaseModel):
    class Meta:
        db_table = 'otp'

    id = IdentityField()
    otp = IntegerField()
    created = DateTimeField()
    expired = CharField()
    user_id = ForeignKeyField(User, lazy_load=True)
    visitor_id = ForeignKeyField(Visitor, lazy_load=True)