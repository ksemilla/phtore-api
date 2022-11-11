from typing import Dict, Any, TypedDict
import strawberry

class BaseSchema:
    def _dict(self) -> Dict[str, Any]:
        return {x:self.__getattribute__(x) for x in dir(self) if not x.startswith("_")}

@strawberry.type
class InsertOneResult:
    acknowledge: bool
    inserted_id: str

class InsertOneResultTypeDict(TypedDict):
    acknowledge: bool
    inserted_id: str