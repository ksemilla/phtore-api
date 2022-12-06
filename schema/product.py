import strawberry
from enum import Enum

from schema.users import TimeStampedSchema, BaseSchema, User

@strawberry.enum
class ProductType(Enum):
    STOCK = "stock"
    LABOR = "labor"
    DOCUMENT = "document"

@strawberry.type
class Product(TimeStampedSchema, BaseSchema):
    _id: strawberry.Private[str]

    entity = str
    code: str
    name: str
    photo: str = ""

    quantity: float = 0
    type: ProductType
    is_active: bool = True
    locked: bool = False

    sell_price: float
    list_price: float

    @strawberry.field
    def id(self) -> str:
        return str(self._id)