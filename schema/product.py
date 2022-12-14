import strawberry
from enum import Enum
from typing import Optional, List

from schema.users import TimeStampedSchema, BaseSchema, User
from schema.datafeed import Datafeed
from database.datafeed import DatafeedManager
from strawberry.scalars import JSON

@strawberry.enum
class ProductType(Enum):
    STOCK = "stock"
    LABOR = "labor"
    DOCUMENT = "document"

@strawberry.type
class Product(TimeStampedSchema, BaseSchema):
    _id: strawberry.Private[str]
    
    entity: str
    code: str
    name: str
    photo: str = ""
    quantity: float = 0
    type: ProductType
    is_active: bool = True
    locked: bool = False
    sell_price: float = 0
    list_price: float = 0

    @strawberry.field
    def id(self) -> str:
        return str(self._id)

    @strawberry.field
    def photo_data(self) -> Datafeed:
        if self.photo:
            datafeed = DatafeedManager.find_by_id(self.photo)
            return Datafeed(**datafeed)
        return Datafeed(_id="", url="", model="", field="", object_id="")

@strawberry.input
class ProductCreateInput(BaseSchema):
    entity: str
    name: str
    code: str
    quantity: float
    type: ProductType
    sell_price: float
    list_price: float

@strawberry.input
class ProductEditInput(BaseSchema):
    name: Optional[str] = strawberry.UNSET
    code: Optional[str] = strawberry.UNSET
    quantity: Optional[float] = strawberry.UNSET
    type: Optional[ProductType] = strawberry.UNSET
    sell_price: Optional[float] = strawberry.UNSET
    list_price: Optional[float] = strawberry.UNSET

@strawberry.input
class ProductFilterOptions(BaseSchema):
    entity: Optional[str] = ""
    name: Optional[str] = strawberry.UNSET

@strawberry.type
class ProductList:
    list: List[Product]
    total_count: int

@strawberry.type
class ItemCategoryChoice:
    name: str

@strawberry.type
class ItemCategory:
    name: str
    choices: List[ItemCategoryChoice]

@strawberry.type
class InstanceAttribute:
    name: str
    value: str

@strawberry.type
class ProductReference:
    name: str
    id: str
    photo_data: Datafeed

@strawberry.type
class ItemInstance:
    attributes: List[InstanceAttribute]
    product: ProductReference

@strawberry.type
class Item:
    _id: strawberry.Private[str]
    entity: str
    name: str
    description: str
    categories: List[ItemCategory]
    instances: List[ItemInstance]
    photo: str = ""

    @strawberry.field
    def id(self) -> str:
        return str(self._id)

    @strawberry.field
    def photo_data(self) -> Datafeed:
        if self.photo:
            datafeed = DatafeedManager.find_by_id(self.photo)
            return Datafeed(**datafeed)
        return Datafeed(_id="", url="", model="", field="", object_id="")

@strawberry.input
class ItemCreateInput(BaseSchema):
    entity: str
    name: str
    description: str
    categories: JSON
    instances: JSON

@strawberry.input
class ItemFilterOptions(BaseSchema):
    entity: Optional[str] = ""
    name: Optional[str] = strawberry.UNSET

@strawberry.type
class ItemList:
    list: List[Item]
    total_count: int

@strawberry.input
class ItemEditInput(BaseSchema):
    name: Optional[str] = strawberry.UNSET
    description: Optional[str] = strawberry.UNSET
    categories: Optional[JSON] = strawberry.UNSET
    instances: Optional[JSON] = strawberry.UNSET

@strawberry.type
class GroupItem:
    entity: str
    name: str