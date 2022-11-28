from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser
from config.settings import Settings
from typing import Optional
import jwt
from database.users import UserManager
from typing import Dict, Any, TypedDict, Optional, Mapping

class User(SimpleUser):
    identity= None
    def __init__(self, username, email="", role="", id="", **kwargs):
        super().__init__(username)
        self.id = id
        self.email = email
        self.role = role

        for k,v in kwargs.items():
            self.__dict__[k] = v

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        token = self.get_token(request)

        if not token:
            return

        try:
            decoded = jwt.decode(token, Settings.APP_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return
        except jwt.InvalidSignatureError:
            return
        except Exception:
            print("got here")
            return

        user = UserManager.find_by_id(decoded['user_id'])
    

        return AuthCredentials(["authenticated"]), User(username=user['email'], id=str(user['_id']),**user)

    def get_header(self, request):
        header: str = request.headers["Authorization"]

        return header

    def get_token(self, request) -> Optional[str]:
        auth_token: str = self.get_header(request)
        partitions = auth_token.split(" ")

        if len(partitions) != 2:
            return

        prefix, token = partitions
        if prefix not in Settings.ALLOWED_AUTHORIZATION_PREFIX:
            return

        return token
