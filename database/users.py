from typing import Mapping, Any
from pymongo import CursorType

from .core import BaseManager

class UserManager(BaseManager):
    resource = "users"