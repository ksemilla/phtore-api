import strawberry

from database.users import UserManager
from database.entity import EntityManager, DeliveryMethodManager
from database.datafeed import DatafeedManager
from database.products import ItemManager
from database.orders import OrderManager
from bson.objectid import ObjectId
from schema.users import Roles, User
import pymongo

@strawberry.field
def run_script() -> str:
    # test = UserManager.update_many({"_id": ObjectId("636e41c9a3990741fdc76067")}, { "role": Roles.ADMIN.value })
    # UserManager.create_index()
    # EntityManager.update_many({"_id": ObjectId("638185e7958b80d7b03f7bb5")}, {"score": 100})
    OrderManager.delete_many()
    # col = EntityManager.get_collection()
    # col.create_index([("score", pymongo.DESCENDING)])
    return ""