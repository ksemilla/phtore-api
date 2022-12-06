from config.settings import Settings
from pymongo import MongoClient, collection as pycol, results, typings, CursorType
from typing import Mapping, Iterable, Any, Optional
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
    def list(cls, **kwargs) -> CursorType:
        filter_arg = kwargs.get('filter', {})
        limit = kwargs.get('limit', 20)
        skip = kwargs.get('skip', 0)
        col = cls.get_collection()
        return col.find(filter=filter_arg, limit=limit, skip=skip)

    @classmethod
    def find_by_id(cls, id: str) -> Mapping[str, Any]:
        col = cls.get_collection()
        obj = col.find_one({ "_id": ObjectId(id) })
        if obj is None:
            raise PyMongoError(f"No {cls.resource} found with id {id}")
        return obj

    @classmethod
    def find(cls, filter: Mapping[str, Any], limit: int = 1) -> Optional[Mapping[str, Any]]:
        col = cls.get_collection()
        obj = col.find(filter, limit=limit)
        return obj

    @classmethod
    def find_one(cls, filter: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        col = cls.get_collection()
        obj = col.find_one(filter=filter)
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
        res = col.find_one_and_update({ "_id": ObjectId(id) }, { "$set":  document})
        return res

    @classmethod
    def update_many(cls, filter: Mapping[str, Any], document: Mapping[str, Any]) -> results.UpdateResult:
        col = cls.get_collection()
        res = col.update_many(filter, { "$set": document })
        return res

    @classmethod
    def delete(cls, id: str) -> typings._DocumentType:
        col = cls.get_collection()
        res = col.find_one_and_delete({ "_id" : ObjectId(id)})
        return res

    @classmethod
    def delete_many(cls) -> None:
        col = cls.get_collection()
        col.delete_many({})
        return