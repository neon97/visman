from peewee import Model
#from vis_app import pg_db
import  vis_app.pg_db as db

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



