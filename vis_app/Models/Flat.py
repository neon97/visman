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

    def serialize(self):
        """Serialize this object to dict/json."""
        d = super(Flat, self).serialize()
        return d
    
    def __str__(self):
        return "Id : {} Flat No: {}, Wing:{}, Society: {}".format(self.id, self.flat_no,self.wing, self.society_id.society_name)