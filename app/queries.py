import environ
import os
from pymongo import MongoClient
class PyMongo:
    
    def __init__(self) :
        path = os.getcwd() + "app\.env"
        env=environ.Env(
            DEBUG=(bool,False)
        )
        environ.Env.read_env(path)

        connection_string = env('connection_string')
        client = MongoClient(connection_string)
        self.db=client['callbot']

    def add(self,collection_name,json_dict):
        collection = self.db[collection_name]
        collection.insert_many([json_dict])
    
    def find(self,collection_name,json_dict):
        collection = self.db[collection_name]
        result = collection.find_one(json_dict)
        return bool(result)

    def get(self,collection_name,attribute,value):
        collection = self.db[collection_name]
        result = collection.find({attribute:value})
        return (result)