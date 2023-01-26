import strawberry
from strawberry.types import Info
from typing import Union
from database.entity import EntityManager, MemberManager, DeliveryMethodManager
from schema.entity import Entity, EntityCreateInput, EntityFilterOptions, EntityList, DeliveryMethodCreateInput, DeliveryMethodFilterOptions, DeliveryMethodList, DeliveryMethod
from schema.core import InsertOneResult
from schema.entity import Entity
from starlette.requests import Request
from starlette.websockets import WebSocket
from typing import List
import pymongo

@strawberry.field
def find_entity_by_slug(slug: str) -> Entity:
    obj = EntityManager.get_entity_by_slug(slug)
    if obj:
        return Entity(**obj)
    return ""

@strawberry.field
def create_entity(info: Info, input: EntityCreateInput) -> InsertOneResult:
    request: Union[Request, WebSocket] = info.context["request"]
    data = input._clean_dict()
    data['owner'] = request.user.id
    data['slug'] = data['name'].lower().replace(" ","-")
    obj = EntityManager.insert(data)
    return InsertOneResult(**obj)

@strawberry.field
def entities(filter: EntityFilterOptions, limit: int = 20, skip: int = 0) -> EntityList:
    cursor = EntityManager.list(filter={'name': { "$regex": filter.name.lower(), '$options': 'i' }}, limit=limit, skip=skip)
    total_count = EntityManager.get_collection().count_documents({'name': { "$regex": filter.name.lower() }})

    return EntityList(
        list=[Entity(**obj) for obj in cursor],
        total_count=total_count
    )

@strawberry.field
def my_entities(info: Info, limit: int = 20, skip: int = 0) -> List[Entity]:
    request: Union[Request, WebSocket] = info.context["request"]
    cursor = EntityManager.list(filter={"owner": request.user.id})
    return [Entity(**obj) for obj in cursor]

@strawberry.field
def entity(slug: str) -> Entity:
    obj = EntityManager.find_one({"slug": slug})
    return Entity(**obj)

@strawberry.field
def remove_banner(slug: str) -> bool:
    EntityManager.update_many({"slug": slug}, {"banner": ""})
    return True

@strawberry.field
def create_delivery_method(input: DeliveryMethodCreateInput) -> InsertOneResult:
    obj = DeliveryMethodManager.insert(input._dict())
    return InsertOneResult(**obj)

@strawberry.field
def delivery_methods(filter: DeliveryMethodFilterOptions, limit: int = 20, skip: int = 0) -> DeliveryMethodList:
    cursor = DeliveryMethodManager.list(filter={"entity": filter.entity } if filter.entity else {}, limit=limit, skip=skip).sort('score', pymongo.ASCENDING)
    total_count = DeliveryMethodManager.get_collection().count_documents({"entity": filter.entity})

    return DeliveryMethodList(
        list=[DeliveryMethod(**obj) for obj in cursor],
        total_count=total_count
    )