import strawberry
from enum import Enum

from typing import Optional, List
from schema.users import TimeStampedSchema, BaseSchema, User
from schema.datafeed import Datafeed
from database.users import UserManager
from database.datafeed import DatafeedManager

@strawberry.type
class Entity(TimeStampedSchema, BaseSchema):
    _id: strawberry.Private[str]
    name: str
    slug: str
    owner: str
    banner: Optional[str] = ""

    score: int = 0
    is_active: bool = True
    locked: bool = False

    @strawberry.field
    def id(self) -> str:
        return str(self._id)

    @strawberry.field
    def owner_data(self) -> User:
        user = UserManager.find_by_id(self.owner)
        return User(**user)

    @strawberry.field
    def banner_data(self) -> Datafeed:
        if self.banner:
            datafeed = DatafeedManager.find_by_id(self.banner)
            return Datafeed(**datafeed)
        return Datafeed(_id="", url="", model="", field="", object_id="")

@strawberry.input
class EntityCreateInput(BaseSchema):
    name: str

@strawberry.input
class EntityFilterOptions(BaseSchema):
    name: Optional[str] = ""

@strawberry.type
class EntityList:
    list: List[Entity]
    total_count: int

@strawberry.enum
class MemberPermissions(Enum):
    VIEW_DASHBOARD = "view.dashboard"

@strawberry.type
class Member(TimeStampedSchema, BaseSchema):
    _id: strawberry.Private[str]

    entity: str
    user: str

    @strawberry.field
    def id(self) -> str:
        return str(self._id)