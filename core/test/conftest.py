# factory registration
from pytest_factoryboy import register

from .factories import BrandFactory, CategoryFactory, ProductFactory


register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)

# although this is registered at CategoryFactory it will be accessed as catetory_factory
