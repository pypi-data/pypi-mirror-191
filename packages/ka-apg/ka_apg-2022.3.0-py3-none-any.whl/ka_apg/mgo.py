import warnings
import pymongo
from pymongo import MongoClient

from ka_utg.com import Com
from ka_utg.log import Log

warnings.filterwarnings("ignore")


class Error(Exception):
    """Base class for other exceptions"""
    pass


class Mgo:
    @staticmethod
    def open():
        cfg_mgo = Com.cfg['mongo']
        try:
            Com.Mgo.client = MongoClient(
                               host=cfg_mgo['host'],
                               port=cfg_mgo['port'],
                               user=cfg_mgo['user'],
                               password=cfg_mgo['password'],
                               database=cfg_mgo['database'])
        except Exception as e:
            Log.error(e, exc_info=True)

    @staticmethod
    def close():
        cfg_mgo = Com.cfg['mongo']
        try:
            Com.Mgo.client = MongoClient(
                               host=cfg_mgo['host'],
                               port=cfg_mgo['port'],
                               user=cfg_mgo['user'],
                               password=cfg_mgo['password'],
                               database=cfg_mgo['database'])
        except Exception as e:
            Log.error(e, exc_info=True)

    class Collection:
        @staticmethod
        def sh(database, collection):
            db = Com.Mgo.client[database]
            return db[collection]

    class Insert:
        @staticmethod
        def one(database, collection, instance):
            collection = Mgo.Collection.sh(database, collection)
            result = collection.insert_one(instance)
            return result

        @staticmethod
        def many(database, collection, instances):
            collection = Mgo.Collection.sh(database, collection)
            result = collection.insert_many(instances)
            return result

    class Query:
        @staticmethod
        def one(database, collection, query):
            collection = Mgo.Collection.sh(database, collection)
            result = collection.insert_one(query)
            return result

        @staticmethod
        def many(database, collection, query):
            collection = Mgo.Collection.sh(database, collection)
            result = collection.insert_one(query)
            return result

    class Index:
        @staticmethod
        def one(database, collection, index, sw_unique=True):
            collection = Mgo.Collection.sh(database, collection)
            index = [('user_id', pymongo.ASCENDING)]
            result = collection.create_index(index, sw_unique)
            return result
