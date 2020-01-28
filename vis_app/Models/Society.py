from peewee import *
from vis_app.Models.BaseModel import BaseModel


class Society(BaseModel):

    class Meta:
        db_table = 'society_table'

    id = IdentityField()
    regd_no = CharField()
    society_name = CharField()
    society_address = CharField()
    total_buildings = IntegerField()
    total_flats = IntegerField()

    def serialize(self):
        """Serialize this object to dict/json."""
        d = super(Society, self).serialize()
        return d

    def __str__(self):
        return "Id : {} Society Name: {}, RegdNo: {}, Address:{}, Total Buildings: {}, Total Flats: {}".format(self.id, self.society_name,
         self.regd_no, self.society_address, self.total_buildings, self.total_flats)