from peewee import IntegerField, IdentityField, CharField, ForeignKeyField, BooleanField, TextField
from vis_app.Models.BaseModel import BaseModel
from vis_app.Models.Society import Society
from vis_app.Models.Flat import Flat


class User(BaseModel):
    class Meta:
        db_table = 'user_table'

    id = IdentityField()
    email = CharField()
    username = CharField()
    first_name = CharField()
    middle_name = CharField()
    last_name = CharField()
    password = CharField()
    society_id = ForeignKeyField(Society, null=False, deferrable=True)
    flat_id = ForeignKeyField(Flat, null=False, deferrable=True)
    isadmin = BooleanField()
    user_entity = IntegerField()
    identification_type = CharField()
    identification_no = CharField()
    photo = TextField()

    EXCLUDE_FIELDS = [password]

    def serialize(self):
        """Serialize this object to dict/json."""
        d = super(User, self).serialize()
        return d

    def __str__(self):
        return "Id : {}, UserName: {}, email: {}, firstname: {}, middlename: {}, lastname:{}, society_id: {}, flat_id:{} , isadmin: {}, user_entity: {}, identification_type: {}, identification_no : {}".format(
            self.id, self.username, self.email, self.first_name, self.middle_name, self.last_name, self.society_id, self.flat_id, self.isadmin, self.user_entity, self.identification_type, self.identification_no)
