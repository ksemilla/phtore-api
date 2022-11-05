import datetime
from typing import Dict, Any, TypedDict
import strawberry

class BaseSchema:
    def _dict(self) -> Dict[str, Any]:
        return {x:self.__getattribute__(x) for x in dir(self) if not x.startswith("_")}

from .users import User

class TimeStampedSchema:
    created_at: datetime.datetime
    created_by: 'User'
    updated_at: datetime.datetime
    updated_by: 'User'

@strawberry.type
class InsertOneResult:
    acknowledge: bool
    inserted_id: str

class InsertOneResultTypeDict(TypedDict):
    ackknowledge: bool
    inserted_id: str