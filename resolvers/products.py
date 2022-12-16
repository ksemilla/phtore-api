import strawberry
from strawberry.types import Info
from schema.product import ProductCreateInput, ProductFilterOptions, ProductList, Product, ProductEditInput
from schema.core import InsertOneResult
from typing import Union
from starlette.requests import Request
from starlette.websockets import WebSocket
from database.products import ProductManager

@strawberry.field
def create_product(info: Info, input: ProductCreateInput) -> InsertOneResult:
    input.type = input.type.value
    # request: Union[Request, WebSocket] = info.context["request"]
    print("input", input)
    data = input._clean_dict()
    print("data", data)
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