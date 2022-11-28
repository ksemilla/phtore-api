import strawberry

from database.users import UserManager
from database.entity import EntityManager
from bson.objectid import ObjectId
from schema.users import Roles, User

@strawberry.field
def run_script() -> str:
    # test = UserManager.update_many({"_id": ObjectId("636e41c9a3990741fdc76067")}, { "role": Roles.ADMIN.value })
    # UserManager.create_index()
    # EntityManager.update_many({}, {"slug": "asd", "owner": {"email":"ahehe", "_id":"636df51aeb87748aad24e702", "password":"asd"}})
    EntityManager.delete_many()
    return ""