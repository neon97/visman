from peewee import Model, PostgresqlDatabase, IntegrityError, DoesNotExist, IntegerField
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

class ConflictDetectedException(Exception): pass


class BaseModel(Model):
    class Meta:
        database = db
        schema = 'visitor_management_schema'

        version = IntegerField(default=1, index=True)

    def save_optimistic(self):
        if not self.id:
            # This is a new record, so the default logic is to perform an
            # INSERT. Ideally your model would also have a unique
            # constraint that made it impossible for two INSERTs to happen
            # at the same time.
            return self.save()

        # Update any data that has changed and bump the version counter.
        field_data = dict(self.__data__)
        # current_version = field_data.pop('version', 1)
        self._populate_unsaved_relations(field_data)
        field_data = self._prune_fields(field_data, self.dirty_fields)
        if not field_data:
            raise ValueError('No changes have been made.')

        ModelClass = type(self)
        field_data['version'] = ModelClass.version + 1  # Atomic increment.

        query = ModelClass.update(**field_data).where(
            # (ModelClass.version == current_version) &
            (ModelClass.id == self.id))
        if query.execute() == 0:
            # No rows were updated, indicating another process has saved
            # a new version. How you handle this situation is up to you,
            # but for simplicity I'm just raising an exception.
            raise ConflictDetectedException()
        else:
            # Increment local version to match what is now in the db.
            self.version += 1
            return True

    EXCLUDE_FIELDS = []

    def serialize(self):
        """Serialize the model into a dict."""
        d = model_to_dict(self, recurse=False, exclude=self.EXCLUDE_FIELDS)
        d["id"] = str(d["id"])  # unification: id is always a string
        return d

    def get_object_or_none(self, model, **kwargs):
        """Retrieve a single object or return None."""
        try:
            return model.get(**kwargs)
        except model.DoesNotExist:
            return None
