from .core import BaseManager

class EntityManager(BaseManager):
    resource = "entity"

    @classmethod
    def get_entity_by_slug(cls, slug: str):
        col = cls.get_collection()
        entity = col.find_one({"slug": slug})
        return entity