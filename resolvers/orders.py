import strawberry
from strawberry.types import Info
from schema.orders import (
    OrderCreateInput,
    OrderFilterOptions,
    OrderList,
    Order,
    OrderItem,
    OrderStatus,
)
from schema.core import InsertOneResult
from schema.datafeed import Datafeed
from typing import Union
from starlette.requests import Request
from starlette.websockets import WebSocket
from database.orders import OrderManager
from typing import List
from bson.objectid import ObjectId

@strawberry.field
def create_order(info: Info, input: OrderCreateInput) -> InsertOneResult:
    input.customer_type = input.customer_type.value
    # request: Union[Request, WebSocket] = info.context["request"]
    data = input._dict()
    data["status"] = OrderStatus.PENDING.value
    order_items = []
    for order_item in data['order_items']:
        order_items.append({
            "product": order_item["product"],
            "sell_price": order_item["sellPrice"],
            "list_price": order_item["listPrice"],
            "quantity": order_item["quantity"]
        })
    data['order_items'] = order_items
    obj = OrderManager.insert(data)
    return InsertOneResult(**obj)

@strawberry.field
def orders(filter: OrderFilterOptions, limit: int = 20, skip: int = 0) -> OrderList:
    cursor = OrderManager.list(filter={"entity": filter.entity}, limit=limit, skip=skip)
    total_count = OrderManager.get_collection().count_documents({"entity": filter.entity})
    
    order_list = []
    for order in cursor:
        order_items = order.pop("order_items")
        order_list.append(Order(**order, order_items=[OrderItem(**obj) for obj in order_items]))
    return OrderList(
        list=order_list,
        total_count=total_count
    )

@strawberry.field
def order(id: str) -> Order:
    obj = OrderManager.find_by_id(id)
    order_items = obj.pop("order_items")
    return Order(**obj, order_items=[OrderItem(**item) for item in order_items])