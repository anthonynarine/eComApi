# UNITTEST:  testing the __str__() dunder method.

"""try to isolate the:

def __str__(self):
    return self.name
    
function as best as possible, and mark
or create some data and then test
that function individually."""

import factory

# bring in model for testing
from core.product.models import Brand, Category, Product, ProductLine

# COMMAND to run test: pytest
# COMMAND to check possible code that needs testing: pytest --cov


# build a factory to test the Category Model.
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # testing currently done on name field only
    # name = "test_category"
    name = factory.Sequence(lambda n: "Category_%d" % n)
    """ this will generate a diffrent number on the name category and increment
        it so for batch creation all the names are not "test_category > category_0..."
        this will allow the field type unique=True to pass this test
    """


# build a factory to test the Brand Model.
class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    # name = "test_brand"
    name = factory.Sequence(lambda n: "Brand_%d" % n)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    description = "test_descriptition"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    """we're going to need to initiate a new brand and a new category in order 
    to associate and to build a product because of the referential integrity,
    because of the relationship that we have built in our database between the
    product table and the brand and category table.
    
    So what's going to happen here is that before we then generate this product,
    we're going to initiate and generate a brand, and then we do the same
    thing for the category as well.
    """
    is_active = True


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "12345"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True
