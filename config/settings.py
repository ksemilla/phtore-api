import os

class Settings:
    APP_KEY = os.environ['APP_KEY']
    MONGO_URI = os.environ['MONGO_URI']
    DB_NAME = os.environ['DB_NAME']