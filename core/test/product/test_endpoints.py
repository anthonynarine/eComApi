# End-to-End testing

import json

import pytest

# import pytest will give access to the db
# the actual db isn't used for testing pytest uses it to generate it's own data

# bring in our Django database for global access (provides access to all tests.)
pytestmark = pytest.mark.django_db


class TestCategoryEndpoint:
    # endpoint to be tested
    endpoint = "/api/category/"

    # create func to rest endpoint
    def test_category_get(self, category_factory, api_client):
        # category_factory and api_client are brought in and called below
        # Arrange (create new factory in this case we are creating 4 new entries)
        category_factory.create_batch(6)

        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        print(json.loads(response.content))  # command to activate this flag pytest -s
        assert len(json.loads(response.content)) == 6
        """parse the data returned and stored in response from our request
        using json.loads(), and then count it. it should = 4 (change batch
        amount to trigger a failed test)."""


class TestBrandEndpoint:
    endpoint = "/api/brand/"

    def test_brand_get(self, brand_factory, api_client):
        brand_factory.create_batch(2)
        response = api_client().get(self.endpoint)  # command to activate this flag pytest -s
        assert response.status_code == 200
        print(json.loads(response.content))
        assert len(json.loads(response.content)) == 2


class TestProductEndpoint:
    endpoint = "/api/product/"

    def test_return_all_product(self, product_factory, api_client):
        product_factory.create_batch(3)
        response = api_client().get(self.endpoint)  # command to activate this flag pytest -s
        assert response.status_code == 200
        print(json.loads(response.content))
        assert len(json.loads(response.content)) == 3

    def test_return_single_product_by_slug(self, product_factory, api_client):
        obj = product_factory(slug="test-slug")
        response = api_client().get(f"{self.endpoint}{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_return_products_by_category_slug(self, category_factory, product_factory, api_client):
        obj = category_factory(slug="test-slug")
        product_factory(category=obj)
        response = api_client().get(f"{self.endpoint}category/{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
