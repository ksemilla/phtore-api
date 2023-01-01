import strawberry
from enum import Enum
from strawberry.file_uploads import Upload
from typing import Optional
from schema.core import BaseSchema
from typing import Optional, List

@strawberry.enum
class Models(Enum):
    ENTITY = "entity"
    PRODUCT = "product"
    ITEM = 'item'

@strawberry.type
class Datafeed(BaseSchema):
    _id: strawberry.Private[str]
    url: str
    model: Models
    field: str
    object_id: str

    @strawberry.field
    def id(self) -> str:
        return str(self._id)

@strawberry.input
class DatafeedInput(BaseSchema):
    file: Upload
    model: Models
    field: str
    object_id: str

@strawberry.type
class DatafeedList:
    list: List[Datafeed]
    total_count: int