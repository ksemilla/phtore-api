import strawberry
from typing import Optional
from enum import Enum
import datetime

from .core import BaseSchema, InsertOneResult

@strawberry.type
class User:
    _id: strawberry.Private[str]
    email: str
    password: strawberry.Private[str]

    name: Optional[str] = strawberry.UNSET
    role: Optional['Roles'] = strawberry.UNSET

    @strawberry.field
    def id(self) -> str:
        return str(self._id)

@strawberry.input
class UserCreate:
    email: str
    password: str

@strawberry.type
class UserCreateResult(InsertOneResult):
    token: str

@strawberry.input
class UserUpdate(BaseSchema):
    email: Optional[str] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET

@strawberry.input
class UserCreate(BaseSchema):
    email: str
    # name: Optional[str]
    password: str

@strawberry.enum
class Roles(Enum):
    ADMIN = "admin"
    USER = "user"

class TimeStampedSchema:
    created_at: datetime.datetime
    created_by: 'User'
    updated_at: datetime.datetime
    updated_by: 'User'