import os
from pymongo import MongoClient
# from pandas import DataFrame
from bson import json_util, BSON
from bson import Binary, Code, ObjectId, Int64, Any
import os, json
import urllib.parse

class NumberLong(int):
    """Representation of the BSON int64 type.

    This is necessary because every integral number is an :class:`int` in
    Python 3. Small integral numbers are encoded to BSON int32 by default,
    but Int64 numbers will always be encoded to BSON int64.

    :Parameters:
      - `value`: the numeric value to represent
    """

    __slots__ = ()

    _type_marker = 18

    def __getstate__(self) -> Any:
        return {}

    def __setstate__(self, state: Any) -> None:
        pass


class Tkmongo():
    def __init__(self, db_name=None):
        """
        :param dbname: The database name in mongo db.
        """
        if db_name is None:
            raise ValueError("DB Name is missing in constructor params.")
        self.service_name = 'mongo'
        self.db_name = db_name
        self.mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
        self.mongo_password = os.getenv("MONGODB_PASSWORD")
        self.http_timeout = 60

    def get_client(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = self.mongo_connection_string.replace("{password}", urllib.parse.quote(self.mongo_password))
        client = MongoClient(CONNECTION_STRING)
        return client

    def get_collection(self, collection_name):
        """
        :param collection_name:
        :return:
        """
        client = self.get_client()
        return client[self.db_name][collection_name]

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def update_document(self, collection_name, query, document):
        collection = self.get_collection(collection_name)
        return collection.update_one(query, document)

    def replace_document(self, collection_name, query, document):
        collection = self.get_collection(collection_name)
        return collection.replace_one(query, document)

    def insert_many_document(self, collection_name, documents):
        collection = self.get_collection(collection_name)
        return collection.insert_many(documents)

    def delete_document(self, db_name, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.delete_one(query)

    def delete_many_documents(self, db_name, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.delete_many(query)

    def fetch_all_document(self, db_name, collection_name):
        collection = self.get_collection(collection_name)
        item_details = collection.find()
        return json.loads(json_util.dumps(list(item_details)))

    def filter_document(self, db_name, collection_name, filter):
        collection = self.get_collection(collection_name)
        item_details = collection.find(filter)
        return json.loads(json_util.dumps(list(item_details)))

    def create_index(self, db_name, collection_name, index_name):
        collection = self.get_collection(collection_name)
        category_index = collection.create_index(index_name)
        return category_index

    def bson_to_json(self, bson_string):
        def mydefault(obj):
            print("Hello")
            if isinstance(obj, NumberLong):
                return int(obj)
            if isinstance(obj, ObjectId):
                print(obj)
                return str(obj)
            if isinstance(obj, str):
                print(obj)
                return int(obj)

        # def cast_values_to_str(data):
        #     result = dict()
        #     for key, value in data.items():
        #         if isinstance(value, dict):
        #             result[key] = cast_values_to_str(value)
        #         elif isinstance(value, NumberLong):
        #             return int(value)
        #         elif isinstance(value, ObjectId):
        #             print(value)
        #         else:
        #             result[key] = str(value)
        #     return result
        print(bson_string)

        json_obj = json.loads(bson_string, object_hook=mydefault)
        # json_str = json_util.dumps(bson_string, default=mydefault)
        # bson_obj = BSON.encode(json_str)
        # print(bson_obj)
        # json_str2 = json_util.dumps(json_obj, default=mydefault)
        # json_data2 = json.dumps(json_value, default=mydefault)
        # json_value2 = json.loads(json_data2)
        # # json_data2 = json.dumps(bson_string)
        # json_data3 = json.dumps(json_value2, default=mydefault)
        print(json_obj)
        # print(json_str2)
        # id = json_value['code']
        return json_obj

    def json_to_bson(self):
        return True

    def string_to_json(self):
        return True



