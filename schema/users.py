import strawberry
from typing import Optional

@strawberry.type
class User:
    _id: strawberry.Private[str]
    email: str
    password: strawberry.Private[str]

    name: Optional[str]

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