from .core import BaseManager

class ProductManager(BaseManager):
    resource: str = "products"

class ItemManager(BaseManager):
    resource = "items"