from config.settings import Settings
from pymongo import MongoClient

class BaseManager:
    db_name = "phtore"
    MONGO_URI = Settings.MONGO_URI
    client = MongoClient(Settings.MONGO_URI)
