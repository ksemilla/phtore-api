from config.settings import Settings
from pymongo import MongoClient, collection as pycol, results, typings
from typing import Mapping, Iterable, Any
from bson.objectid import ObjectId

from pymongo.errors import PyMongoError
from schema.core import InsertOneResultTypeDict

class BaseManager:
    db_name = Settings.DB_NAME
    client: MongoClient = MongoClient(Settings.MONGO_URI)
    resource: str = ""
    collection: pycol.Collection = None

    @classmethod
    def get_collection(cls) -> pycol.Collection:
        if cls.resource == "":
            raise AttributeError("resource field is required")
        return cls.client[cls.db_name][cls.resource]


    @classmethod
    def list(cls) -> Mapping[str, Any]:
        col = cls.get_collection()
        return col.find()

    @classmethod
    def find_by_id(cls, id: str) -> Mapping[str, Any]:
        col = cls.get_collection()
        obj = col.find_one({ "_id": ObjectId(id) })
        if obj is None:
            raise PyMongoError(f"No user found with id {id}")
        return obj

    @classmethod
    def insert(cls, document: Mapping[str, Any]) ->  InsertOneResultTypeDict:
        col = cls.get_collection()
        res = col.insert_one(document)
        return InsertOneResultTypeDict(acknowledge=res.acknowledged, inserted_id=str(res.inserted_id))

    @classmethod
    def insert_many(cls, documents: Iterable[Mapping[str, Any]]) -> results.InsertManyResult:
        col = cls.get_collection()
        res = col.insert_many(documents)
        return res

    @classmethod
    def update(cls, id: str, document: Mapping[str, Any]) -> results.UpdateResult:
        col = cls.get_collection()
        res = col.find_one_and_update({ "_id": ObjectId(id) }, { "$set":  document._dict()})
        return res

    @classmethod
    def delete(cls, id: str) -> typings._DocumentType:
        col = cls.get_collection()
        res = col.find_one_and_delete({ "_id" : ObjectId(id)})
        return res