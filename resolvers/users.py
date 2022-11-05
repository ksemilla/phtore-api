import strawberry

from database.users import UserManager

from schema.users import User, UserUpdate, UserCreate
from schema.core import InsertOneResult
from typing import List
import bcrypt

@strawberry.field
def user(id: str) -> User:
    obj = UserManager.find_by_id(id)
    return User(**obj)

@strawberry.field
def users(self) -> List[User]:
    query = UserManager.list()
    return [User(**obj) for obj in query]

@strawberry.field
def delete_user(self, id: str) -> User:
    obj = UserManager.delete(id)
    return User(**obj)

@strawberry.field
def update_user(self, id: str, data: UserUpdate) -> User:
    obj = UserManager.update(id, data)
    return User(**obj)

@strawberry.field
def create_user(self, data: UserCreate) -> InsertOneResult:

    raw_data = data._dict()
    hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
    raw_data['password'] = hashed_password

    obj = UserManager.insert(raw_data)
    return InsertOneResult(**obj)