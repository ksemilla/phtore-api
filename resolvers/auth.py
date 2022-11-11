import strawberry
import jwt
import datetime
import bcrypt

from schema.auth import LoginInput, LoginResult, VerifyResult
from schema.users import User
from config.settings import Settings
from database.users import UserManager
from graphql import GraphQLError

@strawberry.field
def login(data: LoginInput) -> LoginResult:
    user = UserManager.find_one({"email": data.email})

    if not user:
        return GraphQLError(message="No user found")

    valid: bool = bcrypt.checkpw(data.password.encode("utf-8"), user['password'])
    if not valid:
        return GraphQLError(message="Wrong password")

    encoded_jwt = jwt.encode({
        'user_id': str(user["_id"]),
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=30)
        },
        Settings.APP_KEY)
    return LoginResult(token=encoded_jwt, user=User(**user))

@strawberry.field
def verify_token(token: str) -> VerifyResult:
    try:
        decoded = jwt.decode(token, Settings.APP_KEY, algorithms=["HS256"])
        user = UserManager.find_by_id(decoded['user_id'])
    except jwt.ExpiredSignatureError:
        return GraphQLError(message="Expired token")
    except jwt.InvalidSignatureError:
        return GraphQLError(message="Invalid token")
    except Exception:
        return GraphQLError(message="Cannot decode token")
    
    return VerifyResult(acknowledge=True, user=User(**user))