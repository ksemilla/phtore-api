import os

class Settings:
    MONGO_URI = os.environ['MONGO_URI']
    DB_NAME = os.environ['DB_NAME']