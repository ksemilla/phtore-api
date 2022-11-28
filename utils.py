from typing import Mapping, Any

def object_to_dict(obj: object) -> Mapping[str, Any]:
    return {x:obj.__getattribute__(x) for x in dir(obj) if not x.startswith("_") and obj.__getattribute__(x)}