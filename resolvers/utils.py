import strawberry

from database.users import UserManager
from bson.objectid import ObjectId
from schema.users import Roles

@strawberry.field
def run_script() -> str:
    # test = UserManager.update_many({"_id": ObjectId("636e41c9a3990741fdc76067")}, { "role": Roles.ADMIN.value })
    UserManager.create_index()
    
    return ""