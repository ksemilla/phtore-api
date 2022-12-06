import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
MEDIA_FILES_DIR = str(ROOT_DIR) + "/media"

MEDIA_FILES_URI = "http://localhost:8000/media/"

class Settings:
    ALLOWED_AUTHORIZATION_PREFIX = ('Bearer',)
    APP_KEY = os.environ['APP_KEY']
    MONGO_URI = os.environ['MONGO_URI']
    DB_NAME = os.environ['DB_NAME']
    RESERVED_ENTITY_NAMES = ['my-account,', 'admin', 'stores', 'my-stores']