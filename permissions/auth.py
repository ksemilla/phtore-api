from strawberry.types import Info
from strawberry.permission import BasePermission
from typing import Any, Union
import bcrypt
from starlette.requests import Request
from starlette.websockets import WebSocket
from schema.users import Roles

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context["request"]
        return request.user.is_authenticated

class IsAdmin(BasePermission):
    message = "User is not an admin"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context["request"]
        return request.user.role == Roles.ADMIN.value

class IsAdminOrSelf(BasePermission):
    message = 'You are neither admin nor the user begin updated'

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context["request"]
        _id = kwargs.get("id", "")

        return request.user.role == Roles.ADMIN.value or _id == request.user.id