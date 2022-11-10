import strawberry
from typing import Optional
from enum import Enum

@strawberry.type
class User:
    _id: strawberry.Private[str]
    email: str
    password: strawberry.Private[str]

    name: Optional[str]
    role: 'Roles'

    @strawberry.field
    def id(self) -> str:
        return str(self._id)

@strawberry.input
class UserCreate:
    email: str
    password: str

from .core import BaseSchema

@strawberry.input
class UserUpdate(BaseSchema):
    email: Optional[str] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET

@strawberry.input
class UserCreate(BaseSchema):
    email: str
    name: Optional[str] = strawberry.UNSET
    password: str

@strawberry.enum
class Roles(Enum):
    ADMIN = "admin"
    USER = "user"