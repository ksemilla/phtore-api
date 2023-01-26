import strawberry
from enum import Enum

from typing import Optional, List
from schema.users import TimeStampedSchema, BaseSchema, User
from schema.datafeed import Datafeed
from database.users import UserManager
from database.datafeed import DatafeedManager
from strawberry.scalars import JSON

@strawberry.enum
class CustomerType(Enum):
    USER = "user"
    ENTITY = "entity"

@strawberry.enum
class OrderStatus(Enum):
    PENDING = 1000
    ACCEPTED = 2000
    DELIVERY = 3000
    COMPLETED = 4000
    CANCELLED = 5000
    REJECTED = 6000

@strawberry.type
class OrderItem(BaseSchema):
    product: str
    sell_price: float
    list_price: float
    quantity: float

@strawberry.type
class Order(TimeStampedSchema, BaseSchema):
    _id: strawberry.Private[str]
    entity: str
    customer: str
    customer_type: Optional['CustomerType'] = CustomerType.USER.value
    customer_data: JSON = dict
    shipping_fee: float
    billing_info: JSON = dict
    shipping_same_as_billing: bool
    shipping_info: JSON = dict
    order_items: List[OrderItem]
    status: OrderStatus
    
    @strawberry.field
    def id(self) -> str:
        return str(self._id)    

@strawberry.input
class OrderCreateInput(BaseSchema):
    entity: str
    customer: str
    customer_type: CustomerType
    customer_data: JSON
    shipping_fee: float
    billing_info: JSON
    shipping_same_as_billing: bool
    shipping_info: JSON
    order_items: JSON # TODO REPLACE THIS

@strawberry.input
class OrderFilterOptions(BaseSchema):
    entity: Optional[str] = ""

@strawberry.type
class OrderList:
    list: List[Order]
    total_count: int