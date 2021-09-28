import pymongo

class MongoDbManager_corona:
    _instance = None
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['processed_corona']
 
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
 
    def get_data_from_collection(cls, _query):
        assert cls.database
        return cls.database.find( _query)
 
    def add_data_on_collection(cls, _data):
        if type(_data) is list:
            return cls.database.insert_many(_data)
        else :
            return cls.database.insert_one(_data)

class MongoDbManager_insta:
    _instance = None
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['processed_insta']
 
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
 
    def get_data_from_collection(cls, _query,sub):
        assert cls.database
        return cls.database.find( _query,sub)
 
    def add_data_on_collection(cls, _data):
        if type(_data) is list:
            return cls.database.insert_many(_data)
        else :
            return cls.database.insert_one(_data)