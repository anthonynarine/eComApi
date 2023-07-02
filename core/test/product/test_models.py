import pytest

# import pytest will give access to the db
# the actual db isn't used for testing pytest uses it to generate it's own data

# bring in our Django database for global access (provides access to all tests.)
pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # Act
        obj = category_factory(name="test_cat")
        # Assert (boolean expression will return true or false)
        assert obj.__str__() == "test_cat"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange
        # Act
        obj = brand_factory(name="test_brand")
        # Assert (boolean expression will return true or false)
        assert obj.__str__() == "test_brand"

    ...


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange
        # Act
        obj = product_factory(name="test_product")
        # Assert (boolean expression will return true or false)
        assert obj.__str__() == "test_product"

    ...
    ...
