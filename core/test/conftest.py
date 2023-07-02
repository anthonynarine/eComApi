# factory registration

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import BrandFactory, CategoryFactory, ProductFactory

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)


@pytest.fixture
def api_client():
    return APIClient


# although this is registered at CategoryFactory it will be accessed as catetory_factory
