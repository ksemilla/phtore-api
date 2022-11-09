
from strawberry.types import Info
from strawberry.permission import BasePermission
from typing import Any, Union
import bcrypt
from starlette.requests import Request
from starlette.websockets import WebSocket

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context["request"]
        return request.user.is_authenticated