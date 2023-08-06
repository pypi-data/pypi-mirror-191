import uuid
from pymongo import ReadPreference, WriteConcern


class BaseModel(object):
    db_name = None
    collection = None

    client_mongo = None

    def get_db(self, read_preference=None, write_concern=None):
        w = None
        if write_concern is not None:
            w = WriteConcern(w=write_concern)
        if not self.client_mongo:
            raise Exception('ERROR client_mongo: is {}'.format(self.client_mongo))
        return self.client_mongo.get_database(self.db_name).get_collection(
            self.collection, read_preference=read_preference, write_concern=w
        )

    @staticmethod
    def normalize_uuid(some_uuid):
        if isinstance(some_uuid, str):
            return uuid.UUID(some_uuid)
        return some_uuid

    def find_one(self, query):
        result = (
            self.client_mongo.get_database(self.db_name)
                .get_collection(
                self.collection, read_preference=ReadPreference.SECONDARY_PREFERRED
            ).find_one(query)
        )
        return result
