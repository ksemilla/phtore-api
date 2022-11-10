import strawberry
from typing import Optional

from .users import User

@strawberry.input
class LoginInput:
    email: str
    password: str

@strawberry.type
class LoginResult:
    token: str
    user: Optional[User]