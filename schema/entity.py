import strawberry

from typing import Optional, List
from schema.users import TimeStampedSchema, BaseSchema, User
from database.users import UserManager

@strawberry.type
class Entity(TimeStampedSchema, BaseSchema):
    _id: strawberry.Private[str]
    name: str
    slug: str
    owner: str

    is_active: bool = True
    locked: bool = False

    @strawberry.field
    def id(self) -> str:
        return str(self._id)

    @strawberry.field
    def owner_data(self) -> User:
        user = UserManager.find_by_id(self.owner)
        return User(**user)

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