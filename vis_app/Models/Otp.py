from peewee import *
from vis_app.Models.BaseModel import BaseModel


class OTP(BaseModel):
    class Meta:
        db_table = 'otp'

    id = IdentityField()
    otp = IntegerField()
    created = DateTimeField()
    expired = BooleanField()
    user_id = ForeignKeyField(User, lazy_load=True)
    visitor_id = ForeignKeyField(Visitor, lazy_load=True)