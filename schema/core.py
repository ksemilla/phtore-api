from typing import Dict, Any, TypedDict, Optional, Mapping
import strawberry

class BaseSchema:
    def _dict(self) -> Dict[str, Any]:
        return {x:self.__getattribute__(x) for x in dir(self) if not x.startswith("_")}

    def _clean_dict(self) -> Dict[str, Any]:
        return {x:self.__getattribute__(x) for x in dir(self) if not x.startswith("_") and self.__getattribute__(x)}

@strawberry.type
class InsertOneResult:
    acknowledge: bool
    inserted_id: str

class InsertOneResultTypeDict(TypedDict):
    acknowledge: bool
    inserted_id: str

@strawberry.input
class PageQuery:
    filter: Optional[Dict]
    offset: Optional[int] = 0
    limit: Optional[int] = 10