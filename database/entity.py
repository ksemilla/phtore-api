from .core import BaseManager
from pymongo import CursorType
import pymongo

class EntityManager(BaseManager):
    resource = "entity"

    @classmethod
    def get_entity_by_slug(cls, slug: str):
        col = cls.get_collection()
        entity = col.find_one({"slug": slug})
        return entity

    @classmethod
    def list(cls, **kwargs) -> CursorType:
        filter_arg = kwargs.get('filter', {})
        limit = kwargs.get('limit', 20)
        skip = kwargs.get('skip', 0)
        col = cls.get_collection()
        return col.find(filter=filter_arg, limit=limit, skip=skip).sort("score", pymongo.DESCENDING)

class MemberManager(BaseManager):
    resource = "members"