from peewee import *
from vis_app.Models import BaseModel


class User(BaseModel):
    class Meta:
        db_table = 'user_table'

    id = IdentityField()
    first_name = CharField()
    middle_name = CharField()
    last_name = CharField()
    username = CharField()
    email = CharField()
    password = CharField()
    # society_id = ForeignKeyField(db_column = 'society_id', model=Society, to_field =id, null = False)
    society_id = IntegerField()
    flat_id = IntegerField()
    isadmin = BooleanField()
    user_entity = IntegerField()

    EXCLUDE_FIELDS = [password]

    def serialize(self):
        """Serialize this object to dict/json."""
        d = super(User, self).serialize()
        return d

    # def get_user(att,value):
    #     try:
    #         if att == 'email':
    #             return User.select().where(User.email == value).get()

    #         if att == 'id':
    #             return User.select().where(User.id == value).get()
    #             #return BaseModel.get_object_or_404(User, id=value)

    #     except User.DoesNotExist:
    #         return 'User does not exist'

    def __str__(self):
        return "Id : {} User Name: {}, email: {} ".format(self.id, self.username, self.email)
