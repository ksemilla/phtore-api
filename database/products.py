from .core import BaseManager

class Product(BaseManager):
    resource: str = "products"

class Price(BaseManager):
    resource: str = "prices"