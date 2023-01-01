import strawberry
from strawberry.types import Info
from schema.product import (
    ProductCreateInput, ProductFilterOptions, ProductList, Product, ProductEditInput, ItemCreateInput, ItemFilterOptions, ItemList, Item, ItemCategory, ItemCategoryChoice, InstanceAttribute, ItemInstance, ProductReference, ItemEditInput
)
from schema.core import InsertOneResult
from schema.datafeed import Datafeed
from typing import Union
from starlette.requests import Request
from starlette.websockets import WebSocket
from database.products import ProductManager, ItemManager
from typing import List
from bson.objectid import ObjectId

@strawberry.field
def create_product(info: Info, input: ProductCreateInput) -> InsertOneResult:
    input.type = input.type.value
    # request: Union[Request, WebSocket] = info.context["request"]
    data = input._clean_dict()
    obj = ProductManager.insert(data)
    return InsertOneResult(**obj)


@strawberry.field
def products(filter: ProductFilterOptions, limit: int = 20, skip: int = 0) -> ProductList:
    cursor = ProductManager.list(filter={"entity": filter.entity}, limit=limit, skip=skip)
    total_count = ProductManager.get_collection().count_documents({"entity": filter.entity})
    return ProductList(
        list=[Product(**obj) for obj in cursor],
        total_count=total_count
    )

@strawberry.field
def product(id: str) -> Product:
    obj = ProductManager.find_by_id(id)
    return Product(**obj)

@strawberry.field
def update_product(id: str, input: ProductEditInput) -> Product:
    if input.type: input.type = input.type.value
    obj = ProductManager.update(id, input._clean_dict())
    return Product(**obj)

@strawberry.field
def find_products_by_name(filter: ProductFilterOptions) -> List[Product]:
    cursor = ProductManager.list(filter={"entity": filter.entity, 'name': { "$regex": filter.name.lower(), '$options': 'i' }})
    return [Product(**obj) for obj in cursor]

@strawberry.field
def create_item(info: Info, input: ItemCreateInput) -> InsertOneResult:
    data = input._clean_dict()
    obj = ItemManager.insert(data)
    return InsertOneResult(**obj)

@strawberry.field
def items(filter: ItemFilterOptions, limit: int = 20, skip: int = 0) -> ItemList:
    cursor = ItemManager.list(filter={"entity": filter.entity}, limit=limit, skip=skip)
    total_count = ItemManager.get_collection().count_documents({"entity": filter.entity})

    items = []
    for obj in cursor:
        categories = []
        for category in obj.pop("categories"):
            choices = []
            for choice in category.pop("choices"):
                choices.append(ItemCategoryChoice(**choice))
            categories.append(ItemCategory(**category, choices=choices))

        instances = []
        for instance in obj.pop("instances"):
            attributes = []
            for attribute in instance.pop("attributes"):
                attributes.append(InstanceAttribute(**attribute))
            product = ProductReference(id=instance["product"]["id"], name=instance["product"]["name"], photo_data=Datafeed(_id="", url=instance["product"]["photoData"]["url"], model="", field="", object_id=""))

            instances.append(ItemInstance(attributes=attributes, product=product))
        items.append(Item(**obj, categories=categories, instances=instances))

    return ItemList(
        list=items,
        total_count=total_count
    )

@strawberry.field
def item(id: str) -> Item:
    obj = ItemManager.find_by_id(id)

    categories = []
    for category in obj.pop("categories"):
        choices = []
        for choice in category.pop("choices"):
            choices.append(ItemCategoryChoice(**choice))
        categories.append(ItemCategory(**category, choices=choices))

    instances = []
    for instance in obj.pop("instances"):
        attributes = []
        for attribute in instance.pop("attributes"):
            attributes.append(InstanceAttribute(**attribute))
        product = ProductReference(id=instance["product"]["id"], name=instance["product"]["name"], photo_data=Datafeed(_id="", url=instance["product"]["photoData"]["url"], model="", field="", object_id=""))

        instances.append(ItemInstance(attributes=attributes, product=product))


    return Item(**obj, categories=categories, instances=instances)

@strawberry.field
def update_item(id: str, input: ItemEditInput) -> Item:
    obj = ItemManager.update(id, input._clean_dict())
    return Item(**obj)