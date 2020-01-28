from peewee import Model, PostgresqlDatabase, IntegrityError, DoesNotExist
#from peewee import *
from playhouse.shortcuts import model_to_dict
import db_config.config as config
from vis_app.Models.db import db_connect
#from vis_app import db


# db = PostgresqlDatabase(config.DATABASE_CONFIG['database'],
#                         user=config.DATABASE_CONFIG['user'],
#                         password=config.DATABASE_CONFIG['password'],
#                         host=config.DATABASE_CONFIG['host'],
#                         port=config.DATABASE_CONFIG['port'])

db = db_connect()

class BaseModel(Model):
    class Meta:
        database = db
        schema = 'visitor_management_schema'

    EXCLUDE_FIELDS = []

    def serialize(self):
        """Serialize the model into a dict."""
        d = model_to_dict(self, recurse=False, exclude=self.EXCLUDE_FIELDS)
        d["id"] = str(d["id"]) # unification: id is always a string
        return d

    def get_object_or_none(model, **kwargs):
        """Retrieve a single object or return None."""

        try:
            return model.get(**kwargs)
        except model.DoesNotExist:
            return None



