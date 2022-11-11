import os

class Settings:
    ALLOWED_AUTHORIZATION_PREFIX = ('Bearer',)
    APP_KEY = os.environ['APP_KEY']
    MONGO_URI = os.environ['MONGO_URI']
    DB_NAME = os.environ['DB_NAME']
    FORBIDDEN_ENTITY_NAMES = ['my-account,', 'admin', 'stores']