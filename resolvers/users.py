import strawberry
from typing import List
import bcrypt
import jwt
import datetime
from graphql import GraphQLError

from config.settings import Settings
from database.users import UserManager
from schema.users import User, UserUpdate, UserCreate, UserCreateResult
from schema.core import InsertOneResult
from permissions.auth import (
    IsAuthenticated,
)

@strawberry.field
def user(id: str) -> User:
    obj = UserManager.find_by_id(id)
    return User(**obj)

@strawberry.field
def users() -> List[User]:
    query = UserManager.list()
    return [User(**obj) for obj in query]

@strawberry.field
def delete_user(id: str) -> User:
    obj = UserManager.delete(id)
    return User(**obj)

@strawberry.field
def update_user(id: str, data: UserUpdate) -> User:
    obj = UserManager.update(id, data._dict())
    return User(**obj)

@strawberry.field
def create_user(data: UserCreate) -> UserCreateResult:
    user = UserManager.find_one({"email": data.email})
    if user:
        return GraphQLError(message="Email is already used")

    raw_data = data._dict()
    hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
    raw_data['password'] = hashed_password

    obj = UserManager.insert(raw_data)

    encoded_jwt = jwt.encode({
        'user_id': str(obj["inserted_id"]),
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=30)
        },
        Settings.APP_KEY)

    return UserCreateResult(token=encoded_jwt, **obj)