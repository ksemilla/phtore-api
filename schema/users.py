import strawberry
from typing import Optional, List
from enum import Enum
import datetime

from .core import BaseSchema, InsertOneResult

@strawberry.enum
class Roles(Enum):
    ADMIN = "admin"
    USER = "user"

@strawberry.type
class User:
    _id: strawberry.Private[str]
    email: str
    password: strawberry.Private[str]
    name: Optional[str] = ""
    first_name: str = ""
    last_name: str = ""
    role: Optional['Roles'] = Roles.USER.value
    locked: bool = False
    phone: Optional[str] = ""
    mobile: Optional[str] = ""
    date_of_birth: Optional[str] = ""

    @strawberry.field
    def id(self) -> str:
        return str(self._id)

@strawberry.type
class UserCreateResult(InsertOneResult):
    token: str

@strawberry.input
class UserUpdate(BaseSchema):
    email: Optional[str] = ""
    name: Optional[str] = ""
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    locked: bool = False
    phone: Optional[str] = ""
    mobile: Optional[str] = ""
    date_of_birth: Optional[str] = ""

@strawberry.input
class UserCreate(BaseSchema):
    email: str
    password: str

class TimeStampedSchema:
    created_at: datetime.datetime
    created_by: 'User'
    updated_at: datetime.datetime
    updated_by: 'User'

@strawberry.input
class UserFilterOptions(BaseSchema):
    email: Optional[str] = ""
    name: Optional[str] = ""

@strawberry.type
class UserList:
    list: List[User]
    total_count: int