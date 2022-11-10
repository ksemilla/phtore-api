import strawberry
import jwt
import datetime
import bcrypt

from schema.auth import LoginInput, LoginResult
from schema.users import User
from config.settings import Settings
from database.users import UserManager
from exceptions.auth import WrongPassword
from exceptions.users import NoUserFound

@strawberry.field
def login(data: LoginInput) -> LoginResult:
    user = UserManager.find_one({"email": data.email})

    print("user", user)

    if not user:
        raise NoUserFound("No user found")

    if user:
        valid: bool = bcrypt.checkpw(data.password.encode("utf-8"), user['password'])
        if valid:
            encoded_jwt = jwt.encode({
                'user_id': str(user["_id"]),
                "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=30)
                },
                Settings.APP_KEY)
            return LoginResult(token=encoded_jwt, user=User(**user))
        else:
            raise WrongPassword("Wrong password") 
    

    raise LoginResult(token="", user=None)