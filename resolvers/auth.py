import strawberry
import jwt
import datetime

from schema.auth import Login, LoginResult
from schema.users import User
from config.settings import Settings
from database.users import UserManager

@strawberry.field
def login(data: Login) -> LoginResult:
    user = UserManager.find_one({"email": data.email})

    if user:
        encoded_jwt = jwt.encode({
            'user_id': str(user["_id"]),
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=30)
            },
            Settings.APP_KEY)
        return LoginResult(token=encoded_jwt, user=User(**user))

    return LoginResult(token="", user=None)